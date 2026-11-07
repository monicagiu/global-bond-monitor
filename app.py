import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from bond_math import price, modified_duration, convexity, rate_shock

from data import get_all_yields, to_monthly

st.set_page_config(page_title="Global Bond Monitor", layout="wide")
st.title("Global Government Bond Monitor")
st.caption("10-year government bond yields and spreads. "
           "Source: FRED (Federal Reserve Bank of St. Louis) and OECD. Monthly averages.")


# Download the data once and remember it for 12 hours, so the page loads fast
@st.cache_data(ttl=12 * 60 * 60)
def load_data():
    monthly = to_monthly(get_all_yields())
    monthly.index.name = "Date"
    return monthly


monthly = load_data()

# Let the user choose how far back to look
first_year = int(monthly.dropna().index.year.min())
start_year = st.slider("Show data from", first_year, 2026, 2015)
data = monthly[monthly.index.year >= start_year]

tab_yields, tab_spreads, tab_risk = st.tabs(
    ["10-year yields", "Spreads vs Germany", "Bond risk calculator"])

# ---- Tab 1: 10-year yields ----
with tab_yields:
    countries = ["US 10Y", "Germany 10Y", "Italy 10Y", "UK 10Y"]
    fig = px.line(data[countries], labels={"value": "Yield (%)", "variable": "Bond"})
    st.plotly_chart(fig)

# ---- Tab 2: spreads in basis points (1bp = 0.01%) ----
with tab_spreads:
    spreads = pd.DataFrame({
        "Italy - Germany (BTP-Bund)": (data["Italy 10Y"] - data["Germany 10Y"]) * 100,
        "UK - Germany": (data["UK 10Y"] - data["Germany 10Y"]) * 100,
    })

    # Show the latest available value of each spread as a big number
    col1, col2 = st.columns(2)
    for col, name in zip([col1, col2], spreads.columns):
        latest = spreads[name].dropna()
        col.metric(name, f"{latest.iloc[-1]:.0f} bp",
                   help=f"Latest available month: {latest.index[-1]:%b %Y}")

    fig = px.line(spreads, labels={"value": "Spread (bp)", "variable": "Spread"})
    st.plotly_chart(fig)

    # ---- Tab 3: bond risk calculator ----
with tab_risk:
    st.write("Enter a bond's details to see its price and how sensitive it is "
             "to changes in interest rates. Coupons are paid twice a year.")

    c1, c2, c3 = st.columns(3)
    coupon = c1.number_input("Coupon (% per year)", 0.0, 15.0, 4.0, 0.25) / 100
    years = c2.number_input("Years to maturity", 1, 50, 10)
    ytm = c3.number_input("Yield to maturity (%)", 0.0, 15.0, 4.0, 0.05) / 100
    face = 100

    p = price(face, coupon, years, ytm)
    md = modified_duration(face, coupon, years, ytm)
    cx = convexity(face, coupon, years, ytm)

    m1, m2, m3 = st.columns(3)
    m1.metric("Price (per 100 face value)", f"{p:.2f}")
    m2.metric("Modified duration", f"{md:.2f}",
              help="Approximate % price change for a 1% move in yields")
    m3.metric("Convexity", f"{cx:.1f}",
              help="How much the price-yield relationship curves")

    # Scenario table: what happens to the price if rates move?
    st.markdown("#### Rate shock scenarios")
    rows = []
    for shock in [-200, -100, -50, 50, 100, 200]:
        actual, dur_est, dur_cx_est = rate_shock(face, coupon, years, ytm, shock)
        rows.append({
            "Yield change": f"{shock:+d} bp",
            "Actual price change": f"{actual:+.2%}",
            "Duration estimate": f"{dur_est:+.2%}",
            "Duration + convexity estimate": f"{dur_cx_est:+.2%}",
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True)

    # Chart: the real price-yield curve vs the straight-line duration estimate
    st.markdown("#### Price vs yield")
    yield_range = np.linspace(max(ytm - 0.03, 0.0), ytm + 0.03, 61)
    curve = pd.DataFrame({
        "Yield (%)": yield_range * 100,
        "Actual price": [price(face, coupon, years, y) for y in yield_range],
        "Duration-only estimate": [p * (1 - md * (y - ytm)) for y in yield_range],
    })
    fig = px.line(curve, x="Yield (%)", y=["Actual price", "Duration-only estimate"],
                  labels={"value": "Price", "variable": ""})
    st.plotly_chart(fig)
    st.caption("The gap between the curved line and the straight line is convexity: "
               "when yields fall the bond gains more, and when yields rise it loses "
               "less, than duration alone predicts.")