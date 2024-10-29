import csv
import os

DATA_FILE = "work_hours_data.csv"

def initialize_csv():
    """
    Initializes the CSV file with headers if it doesn't already exist.
    This function is called when the app starts.
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Hours Worked", "Hourly Rate"])
        print(f"{DATA_FILE} initialized successfully.")
    else:
        print(f"{DATA_FILE} already exists.")

def save_data(date, hours, rate):
    """
    Saves a new workday entry to the CSV file.
    Ensures data format is consistent and entries are appended.
    """
    try:
        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, hours, rate])
        print("Data saved successfully.")
    except IOError as e:
        print(f"An error occurred while saving data: {e}")

def load_data():
    """
    Loads work hours data from the CSV file and returns it as a list of dictionaries.
    If the file is missing or empty, returns an empty list.
    """
    entries = []
    try:
        with open(DATA_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert data types to ensure consistency
                try:
                    entry = {
                        "date": row["Date"],
                        "hours": float(row["Hours Worked"]),
                        "rate": float(row["Hourly Rate"])
                    }
                    entries.append(entry)
                except ValueError:
                    print("Data format error: skipping an entry due to invalid values.")
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found; a new file will be created on the next save.")
    except IOError as e:
        print(f"An error occurred while loading data: {e}")

    return entries
