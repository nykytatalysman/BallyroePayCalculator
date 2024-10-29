from tkinter import ttk
from tkcalendar import DateEntry
import tkinter as tk

def create_widgets(root):
    """
    Creates and configures UI components for the main application window.
    Returns a dictionary of widget references for easy access in main.py.
    """
    widgets = {}

    # Title Label for branding
    widgets['title_label'] = ttk.Label(root, text="Ballyroe Pay Calculator", font=("Helvetica", 20, "bold"))
    widgets['title_label'].pack(pady=(10, 10))

    # Initial prompt for user name and hourly rate
    name_prompt_frame = ttk.Frame(root, padding="15 15 15 15")
    widgets['name_prompt_frame'] = name_prompt_frame

    ttk.Label(name_prompt_frame, text="Enter Your Name:", font=("Helvetica", 12)).pack(anchor="w", pady=(0, 5))
    widgets['name_entry'] = ttk.Entry(name_prompt_frame, width=30)
    widgets['name_entry'].pack(pady=(0, 10))

    ttk.Label(name_prompt_frame, text="Enter Hourly Rate (€):", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
    widgets['hourly_rate_entry'] = ttk.Entry(name_prompt_frame, width=20)
    widgets['hourly_rate_entry'].pack(pady=(0, 10))

    widgets['start_button'] = ttk.Button(name_prompt_frame, text="Start", style="Accent.TButton")
    widgets['start_button'].pack(pady=(15, 15))

    # Greeting label displayed after entering name and rate
    widgets['greeting_label'] = ttk.Label(root, text="", font=("Helvetica", 14, "italic"))
    widgets['greeting_label'].pack(pady=(5, 15))

    # Frame for daily entries (date and hours worked)
    input_frame = ttk.Frame(root, padding="10 20 10 20")
    widgets['input_frame'] = input_frame

    ttk.Label(input_frame, text="Select Date:", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
    widgets['date_entry'] = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    widgets['date_entry'].grid(row=0, column=1, padx=(10, 20), pady=5)

    ttk.Label(input_frame, text="Hours Worked:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
    widgets['hours_entry'] = ttk.Entry(input_frame, width=12)
    widgets['hours_entry'].grid(row=1, column=1, padx=(10, 20), pady=5)

    widgets['add_day_button'] = ttk.Button(input_frame, text="Add Workday", style="Accent.TButton")
    widgets['add_day_button'].grid(row=2, column=0, columnspan=2, pady=15)

    # Calculate Button
    widgets['calculate_button'] = ttk.Button(input_frame, text="Calculate Totals", style="Accent.TButton")
    widgets['calculate_button'].grid(row=3, column=0, columnspan=2, pady=15)

    # Frame for displaying totals and averages
    result_frame = ttk.Frame(root, padding="15 20 15 20", relief="solid", borderwidth=1)
    result_frame.pack(fill="x", expand=True, padx=15, pady=(10, 15))

    widgets['total_hours_label'] = ttk.Label(result_frame, text="Total Hours: 0", font=("Helvetica", 12, "bold"))
    widgets['total_hours_label'].pack(anchor="w", pady=(5, 0))

    widgets['total_gross_label'] = ttk.Label(result_frame, text="Total Gross Pay: €0.00", font=("Helvetica", 12, "bold"))
    widgets['total_gross_label'].pack(anchor="w", pady=(5, 0))

    widgets['total_net_label'] = ttk.Label(result_frame, text="Total Net Pay: €0.00", font=("Helvetica", 12, "bold"), foreground="#2F4F4F")
    widgets['total_net_label'].pack(anchor="w", pady=(5, 0))

    widgets['average_label'] = ttk.Label(result_frame, text="Average Net Pay: €0.00", font=("Helvetica", 12, "italic"))
    widgets['average_label'].pack(anchor="w", pady=(5, 10))

    # Text area for displaying saved entries
    widgets['data_display_label'] = ttk.Label(root, text="Saved Entries", font=("Helvetica", 14, "underline"))
    widgets['data_display_label'].pack(pady=(10, 5))

    widgets['data_display'] = tk.Text(root, height=10, width=60, wrap="word", bg="#f9f9f9", font=("Helvetica", 9))
    widgets['data_display'].pack(pady=(0, 15), padx=15)

    # Bottom frame with Save, Load, and Clear Buttons
    bottom_frame = ttk.Frame(root, padding="10 20 10 20")
    bottom_frame.pack(fill="x", expand=True)

    widgets['save_button'] = ttk.Button(bottom_frame, text="Save Data", style="Accent.TButton")
    widgets['save_button'].grid(row=0, column=0, padx=5, pady=5)

    widgets['load_button'] = ttk.Button(bottom_frame, text="Load Data", style="Accent.TButton")
    widgets['load_button'].grid(row=0, column=1, padx=5, pady=5)

    widgets['clear_button'] = ttk.Button(bottom_frame, text="Clear Entries", style="Accent.TButton")
    widgets['clear_button'].grid(row=0, column=2, padx=5, pady=5)

    # Summary and Export Buttons
    widgets['summary_button'] = ttk.Button(bottom_frame, text="Show Weekly Summary", style="Accent.TButton")
    widgets['summary_button'].grid(row=1, column=0, padx=5, pady=5)

    widgets['export_button'] = ttk.Button(bottom_frame, text="Export Summary to PDF", style="Accent.TButton")
    widgets['export_button'].grid(row=1, column=1, padx=5, pady=5)

    return widgets

def display_data_entry(data_display, date, hours, rate):
    """
    Inserts a new entry into the data display text area.

    Parameters:
    - data_display (Text): The Text widget to display saved entries.
    - date (str): The date of the entry.
    - hours (float): Hours worked.
    - rate (float): Hourly rate.
    """
    entry_text = f"Date: {date}, Hours: {hours}, Rate: €{rate}\n"
    data_display.insert(tk.END, entry_text)
