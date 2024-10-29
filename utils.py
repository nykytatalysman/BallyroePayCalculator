from datetime import datetime

# Constants for payroll calculations
STANDARD_RATE_LIMIT = 44000
OVERTIME_THRESHOLD = 40  # Standard weekly hours before overtime
OVERTIME_RATE_MULTIPLIER = 1.5  # Overtime rate (e.g., 1.5x regular rate)
HOLIDAY_RATE_MULTIPLIER = 2.0  # Holiday rate (e.g., 2x regular rate)
PERSONAL_TAX_CREDIT = 2000
EMPLOYEE_TAX_CREDIT = 2000
USC_BANDS = [
    (12012, 0.005), (27382, 0.02), (70044, 0.03), (float('inf'), 0.08)
]

def calculate_gross_pay(hours, rate):
    """
    Calculates gross pay including regular and overtime pay.

    Parameters:
    - hours (float): Number of hours worked.
    - rate (float): Hourly pay rate.

    Returns:
    - dict: Breakdown of regular and overtime pay.
    """
    regular_hours = min(hours, OVERTIME_THRESHOLD)
    overtime_hours = max(hours - OVERTIME_THRESHOLD, 0)
    regular_pay = regular_hours * rate
    overtime_pay = overtime_hours * rate * OVERTIME_RATE_MULTIPLIER
    gross_pay = regular_pay + overtime_pay
    return {"regular_pay": regular_pay, "overtime_pay": overtime_pay, "gross": gross_pay}

def calculate_tax(gross_pay):
    """
    Calculates total tax based on income brackets and personal credits.

    Parameters:
    - gross_pay (float): Gross pay for the period.

    Returns:
    - float: Total tax deducted from gross pay.
    """
    if gross_pay <= STANDARD_RATE_LIMIT:
        income_tax = gross_pay * 0.20
    else:
        income_tax = (STANDARD_RATE_LIMIT * 0.20) + ((gross_pay - STANDARD_RATE_LIMIT) * 0.40)

    # USC calculation
    usc = 0
    previous_band_limit = 0
    for limit, usc_rate in USC_BANDS:
        if gross_pay > previous_band_limit:
            taxable_amount = min(gross_pay, limit) - previous_band_limit
            usc += taxable_amount * usc_rate
            previous_band_limit = limit
        else:
            break

    # Apply tax credits
    total_tax = max(income_tax + usc - (PERSONAL_TAX_CREDIT + EMPLOYEE_TAX_CREDIT), 0)
    return total_tax

def calculate_net_pay(hours, rate):
    """
    Calculates net pay by deducting taxes from gross pay.

    Parameters:
    - hours (float): Number of hours worked.
    - rate (float): Hourly rate of pay.

    Returns:
    - dict: Comprehensive breakdown of net pay calculation.
    """
    gross_info = calculate_gross_pay(hours, rate)
    gross_pay = gross_info["gross"]
    total_tax = calculate_tax(gross_pay)
    net_pay = gross_pay - total_tax

    return {
        "regular_hours": min(hours, OVERTIME_THRESHOLD),
        "overtime_hours": max(hours - OVERTIME_THRESHOLD, 0),
        "regular_pay": gross_info["regular_pay"],
        "overtime_pay": gross_info["overtime_pay"],
        "gross": gross_pay,
        "income_tax": total_tax,
        "net": net_pay
    }

def format_currency(value):
    """
    Formats a float value as currency, rounded to two decimal places.

    Parameters:
    - value (float): The monetary value to format.

    Returns:
    - str: Formatted string with two decimal places, prefixed with €.
    """
    return f"€{value:.2f}"

def calculate_weekly_totals(work_entries):
    """
    Calculates total hours, gross, and net pay for a given week.

    Parameters:
    - work_entries (list of dict): List containing daily entries with 'hours' and 'rate'.

    Returns:
    - dict: Detailed weekly breakdown including gross and net pay.
    """
    total_hours = 0
    total_gross = 0
    total_net = 0
    total_overtime_pay = 0
    total_regular_pay = 0

    for entry in work_entries:
        hours = entry.get("hours", 0)
        rate = entry.get("rate", 0)
        breakdown = calculate_net_pay(hours, rate)

        total_hours += breakdown["regular_hours"] + breakdown["overtime_hours"]
        total_regular_pay += breakdown["regular_pay"]
        total_overtime_pay += breakdown["overtime_pay"]
        total_gross += breakdown["gross"]
        total_net += breakdown["net"]

    return {
        "total_hours": total_hours,
        "total_regular_pay": total_regular_pay,
        "total_overtime_pay": total_overtime_pay,
        "total_gross": total_gross,
        "total_net": total_net,
        "total_deductions": total_gross - total_net
    }

def calculate_holiday_pay(work_entries, holidays):
    """
    Calculates additional holiday pay for specified holidays.

    Parameters:
    - work_entries (list of dict): List containing daily entries with 'date', 'hours', and 'rate'.
    - holidays (list of str): List of dates (in 'YYYY-MM-DD' format) recognized as holidays.

    Returns:
    - float: The total holiday pay.
    """
    holiday_pay = 0
    for entry in work_entries:
        if entry['date'] in holidays:
            holiday_pay += entry['hours'] * entry['rate'] * HOLIDAY_RATE_MULTIPLIER
    return holiday_pay
