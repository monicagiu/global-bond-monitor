import pandas as pd

# FRED lets anyone download a data series as a CSV file using this web address
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"

# The bond yields we want: our name -> FRED's code for that series
SERIES = {
    "US 2Y": "DGS2",
    "US 5Y": "DGS5",
    "US 10Y": "DGS10",
    "US 30Y": "DGS30",
    "Germany 10Y": "IRLTLT01DEM156N",
    "Italy 10Y": "IRLTLT01ITM156N",
    "UK 10Y": "IRLTLT01GBM156N",
}


def get_series(code):
    """Download one series from FRED and return it as a column of numbers."""
    df = pd.read_csv(FRED_URL.format(code), index_col=0, parse_dates=True)
    # Turn any missing values (e.g. bank holidays) into blanks instead of text
    return pd.to_numeric(df.iloc[:, 0], errors="coerce")


def get_all_yields():
    """Download every series and combine them into one table."""
    data = {name: get_series(code) for name, code in SERIES.items()}
    return pd.DataFrame(data)


def to_monthly(yields):
    """Average each month, so daily US data and monthly European data line up."""
    return yields.resample("ME").mean()


if __name__ == "__main__":
    yields = get_all_yields()
    monthly = to_monthly(yields)
    print(monthly.tail(8).round(2))