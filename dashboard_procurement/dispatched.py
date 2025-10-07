import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox

class DispatchedScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.create_style()
        self.create_widgets()

    def create_style(self):
        style = ttk.Style()
        style.theme_use("default")
        
        style.map("Custom.Treeview",
                  background=[("selected", "#397D49")],
                  foreground=[("selected", "white")])

    def create_widgets(self):
        top_frame = tk.Frame(self, bg="lightgrey")
        top_frame.pack(fill="x", padx=20)
        
        tk.Label(top_frame, text="Dispatched Screen", font=("Arial", 16), bg="lightgrey").pack(side="left", pady=20)
        
        from token_utils import get_username
        username = get_username()
        tk.Label(top_frame, text=f"User: {username}", bg="lightgrey", font=("Arial", 10, "bold")).pack(side="right", pady=20)

        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.table = ttk.Treeview(
            table_frame,
            style="Custom.Treeview",
            columns=("name", "email", "request_date", "quantity", "item", "barcode"),
            show="headings"
        )

        self.table.heading("name", text="Name")
        self.table.heading("email", text="Email")
        self.table.heading("request_date", text="Request Date")
        self.table.heading("quantity", text="Quantity")
        self.table.heading("item", text="Item")
        self.table.heading("barcode", text="Barcode")

        self.table.column("name", width=120)
        self.table.column("email", width=180)
        self.table.column("request_date", width=100)
        self.table.column("quantity", width=70, anchor="center")
        self.table.column("item", width=120)
        self.table.column("barcode", width=150)

        self.populate_table()

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.table.pack(fill="both", expand=True)

    def populate_table(self):
        from login import TOKEN
        from config import API_BASE_URL
        url = f"{API_BASE_URL}/api/orders/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                for order in data:
                    if order['final_status'] == 'dispatch':
                        user_name = order['user']['username']
                        user_email = order['user']['email']
                        request_date = order['request_date']
                        quantity = order['quantity']
                        item_names = ', '.join([product['title'] for product in order['product']])
                        barcode = order.get('barcode', '')

                        self.table.insert("", "end", values=(user_name, user_email, request_date, quantity, item_names, barcode))
            else:
                messagebox.showerror("Error", "Failed to retrieve orders data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    app = DispatchedScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()