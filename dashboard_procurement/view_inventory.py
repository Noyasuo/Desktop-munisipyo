import tkinter as tk
from tkinter import ttk
import requests
from login import TOKEN

class ViewInventoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="View Inventory", font=("Arial", 16), bg="lightgrey").pack(pady=20)
        
        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.table = ttk.Treeview(
            table_frame,
            columns=("item", "stock", "category", "barcode"),
            show="headings"
        )

        self.table.heading("item", text="Item")
        self.table.heading("stock", text="Stock")
        self.table.heading("category", text="Category")
        self.table.heading("barcode", text="Barcode")

        self.table.column("item", width=180)
        self.table.column("stock", width=70, anchor="center")
        self.table.column("category", width=120)
        self.table.column("barcode", width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.table.pack(fill="both", expand=True)

        inventory_data = self.fetch_inventory_data()
        self.populate_table(inventory_data)

    def fetch_inventory_data(self):
        from config import API_BASE_URL
        url = f'{API_BASE_URL}/api/products/'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def populate_table(self, inventory_data):
        for product in inventory_data:
            item = product.get("title", "No Title")
            stock = product.get("stock", "N/A")
            category = product.get("category", {}).get("name", "No Category")
            barcode = product.get("barcode", "N/A")

            # Insert data into the table
            self.table.insert("", "end", values=(item, stock, category, barcode))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Adjust the window size to accommodate the table
    app = ViewInventoryScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()