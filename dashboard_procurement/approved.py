import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox
from login import TOKEN


class ApprovedScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_style()  # Create custom styles
        self.create_widgets()

    def create_style(self):
        """Create a custom style for the Treeview."""
        style = ttk.Style()
        style.theme_use("default")

        # Configure Treeview style
        style.configure("Custom.Treeview",
                        background="lightgrey",  # Background color of the treeview
                        foreground="black",
                        rowheight=30,
                        font=("Arial", 10))
        style.map("Custom.Treeview",
                  background=[("selected", "#397D49")],  # Selected row color
                  foreground=[("selected", "white")])    # Selected row text color

    def create_widgets(self):
        # Title label for Approved Request Screen
        tk.Label(self, text="Approved Requests", font=("Arial", 16, "bold")).pack(pady=20)

        # Frame for the table and scrollbar
        table_frame = tk.Frame(self)  # Set background color for the frame
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Create the Treeview widget for the table
        self.tree = ttk.Treeview(table_frame, columns=("Name", "Email", "Request Date", "Quantity", "Price", "Product"), show="headings", style="Custom.Treeview")

        # Define the headings and configure their styles
        headings = ["Name", "Email", "Request Date", "Quantity", "Price", "Product"]
        column_widths = [120, 150, 120, 100, 100, 150]  # Adjusted widths for each column

        for col, width in zip(headings, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width)  # Set width for each column

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add sample data to the table
        self.populate_table()


    def populate_table(self):
        """Populate the table with order data from the API."""
        url = "http://127.0.0.1:8000/api/orders/"
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
                    if order['final_status'] == 'approved':

                        # Extract relevant data from the order object
                        user_name = order['user']['username']  # Assuming 'user' is an ID or object, you can modify this to fetch user details
                        user_email = order['user']['email']  # Same as above, replace with actual user email if nested
                        request_date = order['request_date']
                        quantity = order['quantity']
                        status = order['status']
                        # Assuming product is an array (multiple products in an order)
                        product_names = ', '.join([product['title'] for product in order['product']])
                        product_prices = ', '.join([str(product['price']) for product in order['product']])

                        # Insert data into the table
                        self.tree.insert("", "end", values=(user_name, user_email, request_date, quantity, f"${product_prices}", product_names, status))
            else:
                # If the request fails, show an error message
                messagebox.showerror("Error", "Failed to retrieve orders data.")
        except Exception as e:
            # If any exception occurs, show an error message
            messagebox.showerror("Error", f"An error occurred: {e}")

# To test the ApprovedScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = ApprovedScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
