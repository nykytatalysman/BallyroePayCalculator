from tkinter import messagebox

def is_positive_number(value):
    """
    Checks if a value is a positive number (float or int).
    Returns True if positive, False otherwise.
    """
    try:
        return float(value) > 0
    except ValueError:
        return False

def validate_name(name):
    """
    Validates that the name input is not empty and does not contain numbers.

    Parameters:
    - name (str): The user's name input.

    Returns:
    - bool: True if the name is valid, False otherwise.
    """
    if not name.strip():
        messagebox.showerror("Invalid Input", "Name cannot be empty.")
        return False
    elif any(char.isdigit() for char in name):
        messagebox.showerror("Invalid Input", "Name should not contain numbers.")
        return False
    return True

def validate_hourly_rate(rate):
    """
    Validates that the hourly rate is a positive float.

    Parameters:
    - rate (str): The hourly rate input as a string.

    Returns:
    - bool: True if the rate is valid, False otherwise.
    """
    if not is_positive_number(rate):
        messagebox.showerror("Invalid Input", "Hourly rate must be a positive number.")
        return False
    return True

def validate_hours_worked(hours):
    """
    Validates that hours worked is a positive float.

    Parameters:
    - hours (str): The hours worked input as a string.

    Returns:
    - bool: True if the hours worked is valid, False otherwise.
    """
    if not is_positive_number(hours):
        messagebox.showerror("Invalid Input", "Please enter a positive number for hours worked.")
        return False
    return True

def validate_all_fields(date_entry, hours, rate):
    """
    Validates all input fields before processing.

    Parameters:
    - date_entry (DateEntry): The DateEntry widget containing the selected date.
    - hours (str): The hours worked input as a string.
    - rate (str): The hourly rate input as a string.

    Returns:
    - bool: True if all fields are valid, False otherwise.
    """
    if not date_entry.get_date():
        messagebox.showerror("Invalid Input", "Please select a valid date.")
        return False
    if not validate_hours_worked(hours):
        return False
    if not validate_hourly_rate(rate):
        return False
    return True
