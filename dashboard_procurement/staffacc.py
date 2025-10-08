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
        tk.Label(self, text="Accounts Management", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=20)

        table_frame = tk.Frame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("Name", "Email", "Address", "Contact", "ID No.", "Position", "Username", "Password"), show="headings")

        headings = ["Name", "Email", "Address", "Contact", "ID No.", "Position", "Username", "Password"]
        column_widths = [80, 120, 100, 80, 60, 80, 80, 80]

        for col, width in zip(headings, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#387D3C", foreground="black")
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview", font=("Arial", 10))

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Example data for the table, including password
        self.populate_table()

    def populate_table(self):
        from config import API_BASE_URL
        url = f"{API_BASE_URL}/api/accounts/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }

        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                accounts_data = response.json()
                
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for account in accounts_data:
                    if account["position"] == "dean" or account["position"] == "head":
                        row = (
                            account["first_name"] + " " + account["last_name"],
                            account["email"],
                            account["address"],
                            account["mobile_number"] if account["mobile_number"] else "",
                            account["id_number"] if account["id_number"] else "",
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

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    app = StaffAccountsScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()