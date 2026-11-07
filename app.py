import pandas as pd
import plotly.express as px
import streamlit as st

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

tab_yields, tab_spreads = st.tabs(["10-year yields", "Spreads vs Germany"])

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