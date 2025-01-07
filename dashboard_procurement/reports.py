import tkinter as tk
from tkinter import ttk, messagebox

class ReportsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.create_style()  # Apply custom style for row selection color
        self.create_widgets()

    def create_style(self):
        """Create a custom style to change the selected row color."""
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure Treeview selection color
        style.map("Custom.Treeview",
                  background=[("selected", "#397D49")],  # Selected row color
                  foreground=[("selected", "white")])    # Selected row text color

    def create_widgets(self):
        tk.Label(self, text="Select Month and Year Range for Report", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=20)

        # Frame for dropdowns
        dropdown_frame = tk.Frame(self, bg="lightgrey")
        dropdown_frame.pack(pady=10)

        # Dropdown for selecting "From" month
        self.from_month_var = tk.StringVar()
        tk.Label(dropdown_frame, text="From", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, padx=5, pady=5)
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
        tk.Label(dropdown_frame, text="To", font=("Arial", 12), bg="lightgrey").grid(row=1, column=0, padx=5, pady=5)
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

        # Dropdown for selecting report type (Inserted or Dispatched)
        self.report_type_var = tk.StringVar()
        tk.Label(dropdown_frame, text="Report Type", font=("Arial", 12), bg="lightgrey").grid(row=2, column=0, padx=5, pady=5)
        self.report_type_combobox = ttk.Combobox(dropdown_frame, textvariable=self.report_type_var, font=("Arial", 12), width=15, values=[
            "Inserted", "Dispatched"
        ])
        self.report_type_combobox.set("Select Report Type")  # Default value
        self.report_type_combobox['state'] = 'readonly'  # Make the default text fixed and non-editable
        self.report_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Button to generate report
        self.generate_button = tk.Button(dropdown_frame, text="Generate Report", font=("Arial", 12), command=self.generate_report)
        self.generate_button.grid(row=3, column=0, columnspan=4, pady=10)

        # Create a frame for the table
        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview widget) with custom style
        self.table = ttk.Treeview(
            table_frame,
            style="Custom.Treeview",
            columns=("insert_by", "product", "quantity", "barcode", "date"),
            show="headings"
        )

        # Define headings and column widths
        self.table.heading("insert_by", text="Insert By")
        self.table.heading("product", text="Product")
        self.table.heading("quantity", text="Quantity")
        self.table.heading("barcode", text="Barcode")
        self.table.heading("date", text="Date")

        self.table.column("insert_by", width=120)
        self.table.column("product", width=180)
        self.table.column("quantity", width=70, anchor="center")
        self.table.column("barcode", width=120)
        self.table.column("date", width=100, anchor="center")

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the table into the frame
        self.table.pack(fill="both", expand=True)

    def generate_report(self):
        from_month = self.from_month_var.get()
        from_year = self.from_year_var.get()
        to_month = self.to_month_var.get()
        to_year = self.to_year_var.get()
        report_type = self.report_type_var.get()
        if from_month != "Select Month" and from_year != "Select Year" and to_month != "Select Month" and to_year != "Select Year" and report_type != "Select Report Type":
            # Handle report generation logic here
            print(f"Generating {report_type} report from {from_month} {from_year} to {to_month} {to_year}")
            self.populate_table(report_type, from_month, from_year, to_month, to_year)
        else:
            messagebox.showwarning("Warning", "Please select all fields to generate the report.")

    def populate_table(self, report_type, from_month, from_year, to_month, to_year):
        """Populate the table with sample data."""
        # Clear existing entries in the table
        for item in self.table.get_children():
            self.table.delete(item)

        # Sample data
        sample_data = [
            {"insert_by": "User1", "product": "Product1", "quantity": 10, "barcode": "1234567890", "date": "2023-01-01"},
            {"insert_by": "User2", "product": "Product2", "quantity": 5, "barcode": "0987654321", "date": "2023-02-01"},
            {"insert_by": "User3", "product": "Product3", "quantity": 15, "barcode": "1122334455", "date": "2023-03-01"},
            {"insert_by": "User4", "product": "Product4", "quantity": 20, "barcode": "5566778899", "date": "2023-04-01"},
        ]

        for record in sample_data:
            insert_by = record['insert_by']
            product = record['product']
            quantity = record['quantity']
            barcode = record['barcode']
            date = record['date']

            # Insert data into the table
            self.table.insert("", "end", values=(insert_by, product, quantity, barcode, date))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = ReportsScreen(root)
    app.pack(fill="both", expand=True)
    root.mainloop()