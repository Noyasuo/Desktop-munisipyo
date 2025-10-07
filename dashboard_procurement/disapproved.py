import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox
from login import TOKEN


class DisapprovedScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_style()
        self.create_widgets()

    def create_style(self):
        style = ttk.Style()
        style.theme_use("default")

        
        style.configure("Custom.Treeview",
                        background="lightgrey",
                        foreground="black",
                        rowheight=30,
                        font=("Arial", 10))
        style.map("Custom.Treeview",
                  background=[("selected", "#397D49")],
                  foreground=[("selected", "white")])

    def create_widgets(self):
        
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=20)
        
        
        tk.Label(top_frame, text="Disapproved Requests", font=("Arial", 16, "bold")).pack(side="left", pady=20)
        
        from token_utils import get_username
        username = get_username()
        tk.Label(top_frame, text=f"User: {username}", font=("Arial", 10, "bold")).pack(side="right", pady=20)

        table_frame = tk.Frame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("Name", "Email", "Request Date", "Quantity", "Price", "Product"), show="headings", style="Custom.Treeview")

        headings = ["Name", "Email", "Request Date", "Quantity", "Price", "Product"]
        column_widths = [120, 150, 120, 100, 100, 150]

        for col, width in zip(headings, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.populate_table()
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def populate_table(self):
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
                    if order['final_status'] == 'rejected':
                        user_name = order['user']['username']
                        user_email = order['user']['email']
                        request_date = order['request_date']
                        quantity = order['quantity']
                        status = order['status']
                        product_names = ', '.join([product['title'] for product in order['product']])
                        product_prices = ', '.join([str(product['price']) for product in order['product']])

                        self.tree.insert("", "end", values=(user_name, user_email, request_date, quantity, f"${product_prices}", product_names, status))
            else:
                messagebox.showerror("Error", "Failed to retrieve orders data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = DisapprovedScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
