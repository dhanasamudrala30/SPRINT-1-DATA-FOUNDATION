def operating_cashflow_ratio(operating_activity, net_cash_flow):
    if net_cash_flow == 0:
        return None
    return round(operating_activity / net_cash_flow, 2)



def investment_ratio(investing_activity, operating_activity):
    if operating_activity == 0:
        return None
    return round(abs(investing_activity) / operating_activity, 2)



def financing_ratio(financing_activity, operating_activity):
    if operating_activity == 0:
        return None
    return round(abs(financing_activity) / operating_activity, 2)




def net_cashflow_margin(net_cash_flow, operating_activity):
    if operating_activity == 0:
        return None
    return round((net_cash_flow / operating_activity) * 100, 2)



def is_positive_cashflow(net_cash_flow):
    return net_cash_flow > 0