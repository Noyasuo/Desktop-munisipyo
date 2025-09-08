import tkinter as tk
from tkinter import ttk, messagebox
import requests
from login import TOKEN

class StaffAccountsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Title label for Staff Accounts
        tk.Label(self, text="Accounts Management", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=20)

        # Frame for the table and scrollbar
        table_frame = tk.Frame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Create the Treeview widget for the table
        self.tree = ttk.Treeview(table_frame, columns=("Name", "Email", "Address", "Contact", "ID No.", "Position", "Username", "Password"), show="headings")

        # Define the headings and configure their styles
        headings = ["Name", "Email", "Address", "Contact", "ID No.", "Position", "Username", "Password"]
        column_widths = [80, 120, 100, 80, 60, 80, 80, 80]  # Adjusted widths for each column

        for col, width in zip(headings, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width)  # Set width for each column

        # Set a style for the Treeview widget
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#387D3C", foreground="black")  # Set headings color to the provided green
        style.configure("Treeview", rowheight=30)  # Optional: Set row height
        style.configure("Treeview", font=("Arial", 10))  # Set font for the table content

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Example data for the table, including password
        self.populate_table()

    def populate_table(self):
        """Fetch account data from the API and populate the table."""
        from config import API_BASE_URL
        url = f"{API_BASE_URL}/api/accounts/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }

        try:
            response = requests.get(url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                accounts_data = response.json()
                
                # Clear existing entries in the treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insert each account into the treeview
                for account in accounts_data:
                    # Extract values you want to display in the table
                    if account["position"] == "dean" or account["position"] == "head":
                        row = (
                            account["first_name"] + " " + account["last_name"],
                            account["email"],
                            account["address"],
                            account["mobile_number"] if account["mobile_number"] else "",  # Use mobile_number
                            account["id_number"] if account["id_number"] else "",  # Handle null id_number
                            account["position"],
                            account["username"],
                            "********"
                        )
                        self.tree.insert("", "end", values=row)
                
                print("Table populated successfully.")
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

# Sample usage to test the StaffAccountsScreen independently
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")  # Adjust the window size to accommodate the table
    app = StaffAccountsScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()