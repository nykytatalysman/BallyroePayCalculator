import tkinter as tk
from tkinter import messagebox, filedialog
from data_handler import initialize_csv, load_data, save_data
from ui_components import create_widgets, display_data_entry
from validation import validate_all_fields
from utils import calculate_weekly_totals, format_currency
from fpdf import FPDF, XPos, YPos



print("Application starting...")

class EmployeeData:
    def __init__(self):
        self.name = ""
        self.hourly_rate = 0
        self.entries = []

    def set_employee_info(self, name, hourly_rate):
        self.name = name
        self.hourly_rate = hourly_rate

    def add_entry(self, date, hours):
        self.entries.append({"date": date, "hours": hours, "rate": self.hourly_rate})

    def clear_entries(self):
        self.entries.clear()

    def calculate_totals(self):
        return calculate_weekly_totals(self.entries)

    def save_to_csv(self):
        for entry in self.entries:
            save_data(entry["date"], entry["hours"], entry["rate"])

    def load_from_csv(self):
        self.entries = load_data()


def main():
    # Initialize main application window
    root = tk.Tk()
    root.title("Ballyroe Pay Calculator")
    root.geometry("700x850")
    root.configure(bg="#f0f0f0")
    root.resizable(False, False)

    # Initialize CSV file on first run
    initialize_csv()
    widgets = create_widgets(root)

    employee_data = EmployeeData()  # Use EmployeeData to manage user data and entries

    def start_app():
        name = widgets['name_entry'].get().strip()
        try:
            hourly_rate = float(widgets['hourly_rate_entry'].get())
            if name and hourly_rate > 0:
                employee_data.set_employee_info(name, hourly_rate)
                widgets['name_prompt_frame'].pack_forget()
                widgets['input_frame'].pack(fill="x", expand=True)
                widgets['greeting_label'].config(text=f"Hi {name}! Your hourly rate is €{hourly_rate:.2f}")
                widgets['greeting_label'].pack(pady=5)
            else:
                tk.messagebox.showerror("Invalid Input", "Please enter a valid name and hourly rate.")
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid hourly rate.")

    def add_workday():
        if validate_all_fields(widgets['date_entry'], widgets['hours_entry'].get(), str(employee_data.hourly_rate)):
            date = widgets['date_entry'].get_date().strftime('%Y-%m-%d')
            hours = float(widgets['hours_entry'].get())
            employee_data.add_entry(date, hours)
            display_data_entry(widgets['data_display'], date, hours, employee_data.hourly_rate)
            tk.messagebox.showinfo("Entry Added", f"Entry for {date} added successfully!")

    def calculate_and_display_totals():
        if employee_data.entries:
            totals = employee_data.calculate_totals()
            widgets['total_hours_label'].config(text=f"Total Hours: {totals['total_hours']}")
            widgets['total_gross_label'].config(text=f"Total Gross Pay: €{totals['total_gross']}")
            widgets['total_net_label'].config(text=f"Total Net Pay: {format_currency(totals['total_net'])}")
            average_net_pay = totals['total_net'] / max(len(employee_data.entries), 1)
            widgets['average_label'].config(text=f"Average Net Pay: {format_currency(average_net_pay)}")
            tk.messagebox.showinfo("Calculation Complete", "Totals have been calculated and displayed!")
        else:
            tk.messagebox.showwarning("No Data", "Please add work entries before calculating totals.")

    def clear_entries():
        employee_data.clear_entries()
        widgets['data_display'].delete(1.0, tk.END)
        widgets['total_hours_label'].config(text="Total Hours: 0")
        widgets['total_gross_label'].config(text="Total Gross Pay: €0.00")
        widgets['total_net_label'].config(text="Total Net Pay: €0.00")
        widgets['average_label'].config(text="Average Net Pay: €0.00")
        tk.messagebox.showinfo("Entries Cleared", "All entries have been cleared.")

    def save_data_to_csv():
        if employee_data.entries:
            employee_data.save_to_csv()
            tk.messagebox.showinfo("Data Saved", "Your data has been saved successfully.")
        else:
            tk.messagebox.showwarning("No Data", "There is no data to save.")

    def load_and_display_data():
        employee_data.load_from_csv()
        if employee_data.entries:
            widgets['data_display'].delete(1.0, tk.END)
            for entry in employee_data.entries:
                display_data_entry(widgets['data_display'], entry['date'], entry['hours'], entry['rate'])
            calculate_and_display_totals()
            tk.messagebox.showinfo("Data Loaded", "Data loaded successfully from file.")
        else:
            tk.messagebox.showwarning("No Data", "No data available to load.")

    def show_weekly_summary():
        totals = employee_data.calculate_totals()
        try:
            regular_hours = totals['total_regular_pay'] / employee_data.hourly_rate if employee_data.hourly_rate else 0
            overtime_hours = totals['total_overtime_pay'] / (employee_data.hourly_rate * 1.5) if employee_data.hourly_rate else 0
            summary_text = (
                f"Total Hours: {totals['total_hours']}\n"
                f"Regular Hours: {regular_hours:.2f}\n"
                f"Overtime Hours: {overtime_hours:.2f}\n"
                f"Gross Pay: €{totals['total_gross']}\n"
                f"Total Deductions: €{totals['total_deductions']}\n"
                f"Net Pay: €{totals['total_net']}\n"
            )
            tk.messagebox.showinfo("Weekly Summary", summary_text)
        except ZeroDivisionError:
            tk.messagebox.showerror("Calculation Error", "Hourly rate cannot be zero when calculating summary.")

    def export_summary_to_pdf():
        totals = employee_data.calculate_totals()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)  # Replacing "Arial" with "Helvetica"

        pdf.cell(200, 10, text="Ballyroe Pay Calculator - Weekly Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
                 align="C")
        pdf.cell(200, 10, text=f"Name: {employee_data.name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 10, text=f"Hourly Rate: EUR{employee_data.hourly_rate}", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
                 align="L")
        pdf.cell(200, 10, text=f"Total Hours: {totals['total_hours']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 10, text=f"Gross Pay: EUR{totals['total_gross']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        pdf.cell(200, 10, text=f"Total Deductions: EUR{totals['total_deductions']}", new_x=XPos.LMARGIN,
                 new_y=YPos.NEXT, align="L")
        pdf.cell(200, 10, text=f"Net Pay: EUR{totals['total_net']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")

        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            pdf.output(filename)
            tk.messagebox.showinfo("Export Success", f"Summary exported to {filename} successfully!")

    # Assign button commands
    widgets['start_button'].config(command=start_app)
    widgets['add_day_button'].config(command=add_workday)
    widgets['calculate_button'].config(command=calculate_and_display_totals)
    widgets['clear_button'].config(command=clear_entries)
    widgets['save_button'].config(command=save_data_to_csv)
    widgets['load_button'].config(command=load_and_display_data)
    widgets['summary_button'].config(command=show_weekly_summary)
    widgets['export_button'].config(command=export_summary_to_pdf)

    # Show initial prompt frame
    widgets['name_prompt_frame'].pack(fill="x", expand=True)

    # Footer text
    footer_label = tk.Label(root, text="Made by Nikita", font=("Helvetica", 8, "italic"), bg="#f0f0f0")
    footer_label.pack(side="bottom", anchor="e", padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
