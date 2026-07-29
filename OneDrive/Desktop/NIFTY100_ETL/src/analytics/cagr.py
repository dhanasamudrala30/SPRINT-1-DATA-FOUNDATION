from math import pow


def calculate_cagr(begin_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Returns:
        float : CAGR percentage
        None  : Invalid input
    """

    if begin_value <= 0 or end_value <= 0 or years <= 0:
        return None

    cagr = (pow(end_value / begin_value, 1 / years) - 1) * 100
    return round(cagr, 2)