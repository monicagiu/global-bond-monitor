# Global Government Bond Monitor

**Live dashboard:** https://monicagiu-bond-monitor.streamlit.app

A Python dashboard tracking 10-year government bond yields and spreads for the US, Germany, Italy and the UK.

## Why I built this
Growing up in Italy, I heard about the "spread" on the evening news long before I understood what it meant. During my MSc at LSE, the Asset Markets course gave me the tools to understand bond pricing and yields, and I wanted to go a step further by tracking real markets myself. This project is my way of building hands-on fixed income experience as I move from audit into investment management, and of practising Python and GitHub Copilot along the way.

## What it shows
- **10-year yields:** monthly yields for the US, Germany, Italy and the UK
- **Spreads vs Germany:** the Italy–Germany (BTP–Bund) and UK–Germany spreads in basis points, with the latest available values
- **Bond risk calculator:** price, modified duration and convexity for any fixed-coupon bond, with rate shock scenarios (±50 to ±200bp) comparing the actual price change with duration and duration-plus-convexity estimates

## What I noticed
- The BTP–Bund spread has narrowed from above 300bp in 2013 to around 80bp in 2026, the lowest level in the period shown. Markets now see Italian debt as far less risky than a decade ago.
- The biggest spikes, in 2018 and 2022, line up with Italy's budget dispute with the EU and the start of ECB rate hikes.
- What surprised me most: since 2024, the UK has paid a wider spread over Germany than Italy has (around 177bp vs 80bp).
- For a 30-year bond, a 2% fall in yields raises the price by about 45%, while a 2% rise lowers it by only about 28%. This is positive convexity, and duration alone misses it.

## Data
- US Treasury yields: FRED (Federal Reserve Bank of St. Louis), daily, averaged to monthly
- Germany, Italy and UK 10-year yields: OECD via FRED, monthly. European data is published with a one-to-two month delay

## What I learned
- How to source and clean real market data, including combining daily US data with monthly European data
- How to turn analysis into an interactive tool that others can use

## Built with
Python, pandas, Plotly and Streamlit. Developed in GitHub Codespaces with GitHub Copilot.

---
Built by Monica Giuliano
