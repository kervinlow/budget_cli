# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_budget.ipynb.

# %% auto 0
__all__ = ['main']

# %% ../nbs/00_budget.ipynb 3
from sys import exit
from datetime import date, timedelta
from array import array
from ast import literal_eval
from fastcore.script import *

# %% ../nbs/00_budget.ipynb 6
@call_parse
def main(budget:float,        # The budget amount per day
         start_date:str,      # The start date of the calculation period; it is expected to be in the ISO 8601 format
         end_date:str,        # The end date of the calculation period; it is expected to be in the ISO 8601 format
         days_in_week:int=6,  # The number of consecutive days in a week (starting from Monday) to include in the budget
         weights:str=None,    # The weight to apply for each day of a week, and specified as '[x0, .. , xn]', where x0..xn are numbers; this will override --days_in_week
         amounts:str=None):   # The budget amount for each day of a week, and specified as '[x0, .. , xn]', where x0..xn are numbers; the budget amount per day that was specified will be ignored
    """Return the total budget for the calculation period from the start date to the end date (inclusive)."""
    total_budget = 0.0
    try:
        start = date.fromisoformat(start_date)
    except ValueError:
        exit('budget: error: start_date is not in ISO date format\n')
    try:
        end = date.fromisoformat(end_date)
    except ValueError:
        exit('budget: error: end_date is not in ISO date format\n')
    if end < start:
        exit('budget: error: end_date is not after start_date\n')
    elif end == start:
        total_budget = budget
    else:
        if days_in_week < 1 or days_in_week > 7:
            exit('budget: error: days_in_week must be a value from 1 to 7\n')
        ws = array('d')
        if weights is None:  # use the command-line argument, days_in_week, to create the weights that are applied for calculating the total budget
            for d in range(7):
                if d in range(days_in_week):
                    ws.append(1.0)
                else:
                    ws.append(0.0)
        else:  # use the command-line argument, weights, as the weights to be applied when calculating the total budget
            try:
                ls = literal_eval(weights)
            except:
                exit("budget: error: WEIGHTS should be a string that represents a list of numbers only (each element of the list can be an integer or a real number)\n")
            if len(ls) != 7:
                exit('budget: error: WEIGHTS should be a list with a length of 7 elements (because there are 7 days in a week)\n')
            ws.fromlist(ls)
        amts = array('d')
        if amounts is None:  # use the command-line argument, budget, to create the daily budget amounts for calculating the total budget
            for d in range(7):
                amts.append(budget)
        else:  # use the command-line argument, amounts, as the daily budget amounts to be applied when calculating the total budget
            try:
                ls = literal_eval(amounts)
            except:
                exit("budget: error: AMOUNTS should be a string that represents a list of numbers only (each element of the list can be an integer or a real number)\n")
            if len(ls) != 7:
                exit('budget: error: AMOUNTS should be a list with a length of 7 elements (because there are 7 days in a week)\n')
            amts.fromlist(ls)
        period = end - start
        dates = [start + timedelta(days=i) for i in range(period.days + 1)]
        for dt in dates:
            total_budget += amts[dt.weekday()] * ws[dt.weekday()]
    return total_budget