def net_profit_margin(net_profit, sales):
    if sales is None or sales == 0:
        return None
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    if sales is None or sales == 0:
        return None
    return round((operating_profit / sales) * 100, 2)


def check_opm(calculated_opm, source_opm):
    if calculated_opm is None or source_opm is None:
        return False
    return abs(calculated_opm - source_opm) > 1


def return_on_equity(net_profit, equity_capital, reserves):
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    operating_profit,
    other_income,
    depreciation,
    equity_capital,
    reserves,
    borrowings,
):
    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    ebit = operating_profit + other_income - depreciation

    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit, total_assets):
    if total_assets is None or total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)


# -------------------------------------------------------------------------------------

def debt_to_equity(total_debt, equity_capital, reserves):
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(total_debt / equity, 2)


def is_high_leverage(dte_ratio, threshold=2.0):
    if dte_ratio is None:
        return False

    return dte_ratio > threshold


def interest_coverage(ebit, interest_expense):
    if interest_expense is None or interest_expense <= 0:
        return None

    return round(ebit / interest_expense, 2)


def is_debt_free(total_debt):
    return total_debt == 0


def net_debt(total_debt, cash):
    return round(total_debt - cash, 2)


def asset_turnover(sales, total_assets):
    if total_assets is None or total_assets <= 0:
        return None

    return round(sales / total_assets, 2)