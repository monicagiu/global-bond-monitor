import numpy as np

# All bonds here pay coupons twice a year (freq=2), like US Treasuries.
# Prices are per 100 of face value. Rates are decimals (4% = 0.04).


def cash_flows(face, coupon_rate, years, freq=2):
    """List every payment the bond makes: coupons, plus the face value at the end."""
    n = int(round(years * freq))              # number of payments
    times = np.arange(1, n + 1) / freq        # when each payment happens, in years
    cfs = np.full(n, face * coupon_rate / freq)  # each coupon payment
    cfs[-1] += face                           # final payment also repays the face value
    return times, cfs


def present_values(face, coupon_rate, years, ytm, freq=2):
    """Discount each payment back to today using the yield."""
    times, cfs = cash_flows(face, coupon_rate, years, freq)
    return times, cfs / (1 + ytm / freq) ** (times * freq)


def price(face, coupon_rate, years, ytm, freq=2):
    """Bond price = sum of the present values of all payments."""
    _, pv = present_values(face, coupon_rate, years, ytm, freq)
    return float(pv.sum())


def macaulay_duration(face, coupon_rate, years, ytm, freq=2):
    """Weighted-average time (in years) until you receive the bond's payments."""
    times, pv = present_values(face, coupon_rate, years, ytm, freq)
    return float((times * pv).sum() / pv.sum())


def modified_duration(face, coupon_rate, years, ytm, freq=2):
    """Approximate % price change for a 1% change in yield."""
    return macaulay_duration(face, coupon_rate, years, ytm, freq) / (1 + ytm / freq)


def convexity(face, coupon_rate, years, ytm, freq=2):
    """How much duration itself changes as yields move (the curve in the price-yield line)."""
    times, pv = present_values(face, coupon_rate, years, ytm, freq)
    return float((pv * times * (times + 1 / freq)).sum()
                 / (pv.sum() * (1 + ytm / freq) ** 2))


def rate_shock(face, coupon_rate, years, ytm, shock_bp, freq=2):
    """Price change if yields move by shock_bp basis points: actual vs. estimates."""
    dy = shock_bp / 10000                     # e.g. 100bp -> 0.01
    p0 = price(face, coupon_rate, years, ytm, freq)
    p1 = price(face, coupon_rate, years, ytm + dy, freq)
    md = modified_duration(face, coupon_rate, years, ytm, freq)
    cx = convexity(face, coupon_rate, years, ytm, freq)
    actual = (p1 - p0) / p0
    duration_only = -md * dy
    duration_and_convexity = -md * dy + 0.5 * cx * dy ** 2
    return actual, duration_only, duration_and_convexity


if __name__ == "__main__":
    # Quick check: a 10-year 4% bond yielding 4% should be priced at 100
    print("Price:", round(price(100, 0.04, 10, 0.04), 2))
    print("Modified duration:", round(modified_duration(100, 0.04, 10, 0.04), 2))
    print("Convexity:", round(convexity(100, 0.04, 10, 0.04), 1))
    print("+100bp shock:", [f"{x:.2%}" for x in rate_shock(100, 0.04, 10, 0.04, 100)])