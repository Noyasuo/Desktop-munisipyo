import tkinter as tk
from tkinter import ttk, messagebox

class ReportsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Month and Year Range for Report", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=20)

        # Frame for dropdowns
        dropdown_frame = tk.Frame(self, bg="lightgrey")
        dropdown_frame.pack(pady=10)

        # Dropdown for selecting "From" month
        self.from_month_var = tk.StringVar()
        tk.Label(dropdown_frame, text="From Month:", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, padx=5, pady=5)
        self.from_month_combobox = ttk.Combobox(dropdown_frame, textvariable=self.from_month_var, font=("Arial", 12), width=15, values=[
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
        ])
        self.from_month_combobox.set("Select Month")  # Default value
        self.from_month_combobox['state'] = 'readonly'  # Make the default text fixed and non-editable
        self.from_month_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Dropdown for selecting "From" year
        self.from_year_var = tk.StringVar()
        tk.Label(dropdown_frame, text="", font=("Arial", 12), bg="lightgrey").grid(row=0, column=2, padx=5, pady=5)
        self.from_year_combobox = ttk.Combobox(dropdown_frame, textvariable=self.from_year_var, font=("Arial", 12), width=10, values=[
            "2022", "2023", "2024", "2025", "2026"
        ])
        self.from_year_combobox.set("Select Year")  # Default value
        self.from_year_combobox['state'] = 'readonly'  # Make the default text fixed and non-editable
        self.from_year_combobox.grid(row=0, column=3, padx=5, pady=5)

        # Dropdown for selecting "To" month
        self.to_month_var = tk.StringVar()
        tk.Label(dropdown_frame, text="To Month:", font=("Arial", 12), bg="lightgrey").grid(row=1, column=0, padx=5, pady=5)
        self.to_month_combobox = ttk.Combobox(dropdown_frame, textvariable=self.to_month_var, font=("Arial", 12), width=15, values=[
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
        ])
        self.to_month_combobox.set("Select Month")  # Default value
        self.to_month_combobox['state'] = 'readonly'  # Make the default text fixed and non-editable
        self.to_month_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Dropdown for selecting "To" year
        self.to_year_var = tk.StringVar()
        tk.Label(dropdown_frame, text="", font=("Arial", 12), bg="lightgrey").grid(row=1, column=2, padx=5, pady=5)
        self.to_year_combobox = ttk.Combobox(dropdown_frame, textvariable=self.to_year_var, font=("Arial", 12), width=10, values=[
            "2022", "2023", "2024", "2025", "2026"
        ])
        self.to_year_combobox.set("Select Year")  # Default value
        self.to_year_combobox['state'] = 'readonly'  # Make the default text fixed and non-editable
        self.to_year_combobox.grid(row=1, column=3, padx=5, pady=5)

        # Button to generate report
        self.generate_button = tk.Button(self, text="Generate Report", font=("Arial", 12), command=self.generate_report)
        self.generate_button.pack(pady=20)

    def generate_report(self):
        from_month = self.from_month_var.get()
        from_year = self.from_year_var.get()
        to_month = self.to_month_var.get()
        to_year = self.to_year_var.get()
        if from_month != "Select Month" and from_year != "Select Year" and to_month != "Select Month" and to_year != "Select Year":
            # Handle report generation logic here
            print(f"Generating report from {from_month} {from_year} to {to_month} {to_year}")
            messagebox.showinfo("Report", f"Report from {from_month} {from_year} to {to_month} {to_year} generated successfully!")
        else:
            messagebox.showwarning("Warning", "Please select both 'From' and 'To' months and years to generate the report.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = ReportsScreen(root)
    app.pack(fill="both", expand=True)
    root.mainloop()