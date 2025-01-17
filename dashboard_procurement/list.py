import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox

class ListScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="lightgrey")
        self.master = master
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
        # Title label
        tk.Label(self, text="List Screen", font=("Arial", 16), bg="lightgrey").pack(pady=20)

        # Create a frame for the table
        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview widget) with custom style
        self.table = ttk.Treeview(
            table_frame,
            style="Custom.Treeview",
            columns=("name", "email", "request_date", "quantity", "product", "decision"),
            show="headings"
        )

        # Define headings and column widths
        self.table.heading("name", text="Name")
        self.table.heading("email", text="Email")
        self.table.heading("request_date", text="Request Date")
        self.table.heading("quantity", text="Quantity")
        self.table.heading("product", text="Item")
        self.table.heading("decision", text="Decision")

        self.table.column("name", width=120)
        self.table.column("email", width=180)
        self.table.column("request_date", width=100)
        self.table.column("quantity", width=70, anchor="center")
        self.table.column("product", width=120)
        self.table.column("decision", width=100, anchor="center")

        # Add sample data to the table
        self.populate_table()

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the table into the frame
        self.table.pack(fill="both", expand=True)

    def populate_table(self):
        from login import TOKEN

        """Populate the table with order data from the API."""
        url = "http://52.62.183.28/api/orders/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'  # Replace with your actual token
        }
        
        try:
            # Make the GET request to the API
            response = requests.get(url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                
                for order in data:
                    if order['final_status'] == 'approved' or order['final_status'] == 'rejected':
                        user_name = order['user']['username']  # Assuming 'user' is an ID or object, you can modify this to fetch user details
                        user_email = order['user']['email']  # Same as above, replace with actual user email if nested
                        request_date = order['request_date']
                        quantity = order['quantity']
                        status = order['final_status']
                        # Assuming product is an array (multiple products in an order)
                        product_names = ', '.join([product['title'] for product in order['product']])

                        # Insert data into the table
                        self.table.insert("", "end", values=(user_name, user_email, request_date, quantity, product_names, status))
            else:
                # If the request fails, show an error message
                messagebox.showerror("Error", "Failed to retrieve orders data.")
        except Exception as e:
            # If any exception occurs, show an error message
            messagebox.showerror("Error", f"An error occurred: {e}")

# To test the ListScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    app = ListScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()