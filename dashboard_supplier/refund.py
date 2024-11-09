import tkinter as tk
from tkinter import ttk
import requests
import requests
from tkinter import messagebox

class RefundScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#f5f5f5")
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
        label = tk.Label(self, text="Refunds", font=("Arial", 18), bg="#f5f5f5")
        label.pack(pady=20)

        # Create a frame for the table
        table_frame = tk.Frame(self, bg="#f5f5f5")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview widget) with custom style
        self.table = ttk.Treeview(
            table_frame,
            style="Custom.Treeview",
            columns=("order_no", "name", "email", "invoice_no", "product_title", "product_qty",
                     "order_date", "total_amount", "status", "refund_process"),
            show="headings"
        )

        # Define headings and column widths
        self.table.heading("order_no", text="Order No.")
        self.table.heading("name", text="Name")
        self.table.heading("email", text="Email")
        self.table.heading("invoice_no", text="Invoice No.")
        self.table.heading("product_title", text="Product Title")
        self.table.heading("product_qty", text="Product Qty")
        self.table.heading("order_date", text="Order Date")
        self.table.heading("total_amount", text="Total Amount")
        self.table.heading("status", text="Status")
        self.table.heading("refund_process", text="Refund Process")

        # Set column widths
        self.table.column("order_no", width=100, anchor="center")
        self.table.column("name", width=150)
        self.table.column("email", width=200)
        self.table.column("invoice_no", width=150)
        self.table.column("product_title", width=150)
        self.table.column("product_qty", width=100, anchor="center")
        self.table.column("order_date", width=120)
        self.table.column("total_amount", width=120, anchor="center")
        self.table.column("status", width=100)
        self.table.column("refund_process", width=120)

        # Add sample data to the table
        self.populate_table()

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the table into the frame
        self.table.pack(fill="both", expand=True)

        # Action Buttons
        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.pack(fill="x", padx=20, pady=10)

        # Accept Refund Button
        self.accept_button = tk.Button(button_frame, text="Accept Refund", width=20, command=self.accept_refund)
        self.accept_button.pack(side="left", padx=10)

        # Decline Refund Button
        self.decline_button = tk.Button(button_frame, text="Decline Refund", width=20, command=self.decline_refund)
        self.decline_button.pack(side="left", padx=10)

    def populate_table(self):
        from login import TOKEN
        """Populates the table with refund data from the API."""
        # API URL and headers
        url = 'http://127.0.0.1:8000/api/orders/refund/'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }

        # Fetch data from the API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            refunds = response.json()

            # Iterate over the data and insert it into the table
            for refund in refunds:
                # Extract relevant data from the response
                order_no = refund['id']
                name = refund['user']['first_name'] + " " + refund['user']['last_name']
                email = refund['user']['email']
                invoice_no = refund['order'].get('invoice_number', 'N/A')
                product_title = refund['order']['product'][0]['title']  # Assuming only one product per order
                product_qty = refund['order']['quantity']
                order_date = refund['order']['request_date']
                total_amount = f"${refund['refund_amount']}"  # Format refund amount as currency
                status = refund['order']['status']
                refund_process  = refund['status']

                # Insert the refund data into the table
                self.table.insert("", "end", values=(
                    order_no,
                    name,
                    email,
                    invoice_no,
                    product_title,
                    product_qty,
                    order_date,
                    total_amount,
                    status,
                    refund_process
                ))
        else:
            print(f"Error fetching refund data: {response.status_code}")

    def accept_refund(self):
        from login import TOKEN
        
        """Handle the action of accepting a refund by updating its status via API."""
        selected_item = self.table.selection()
        if selected_item:
            refund = self.table.item(selected_item)["values"]
            print(refund)
            order_no = refund[0]

            # Prepare the data to update the refund status
            data = {
                "status": "approved",
                "refund_amount": refund[0]
            }

            # API URL for updating refund status (replace with actual URL)
            url = f"http://127.0.0.1:8000/api/orders/{order_no}/refund/"

            headers = {
                "Authorization": f"Token {TOKEN}",  # Replace <your_token> with actual token
                "Content-Type": "application/json"
            }

            try:
                # Make the PATCH request to the API to update the refund status
                response = requests.put(url, json=data, headers=headers)

                print(response.text)

                if response.status_code == 200:
                    # Update the status in the table
                    self.table.item(selected_item, values=(refund[0], refund[1], refund[2], refund[3], refund[4], 
                                                        refund[5], refund[6], refund[7], "Accepted", refund[9]))
                    print(f"Refund accepted for Order No: {order_no}")
                    messagebox.showinfo("Success", f"Refund for Order No {order_no} has been accepted successfully.")
                else:
                    print("Failed to accept the refund:", response.json())
                    messagebox.showerror("Error", f"Failed to accept refund for Order No {order_no}.")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while making the API request: {e}")
                messagebox.showerror("Error", "An error occurred while processing the refund. Please try again.")
        else:
            print("No row selected")
            messagebox.showwarning("Selection", "Please select a refund to accept.")

    def decline_refund(self):
        """Handle the action of rejected a refund by updating its status via API."""
        selected_item = self.table.selection()
        if selected_item:
            refund = self.table.item(selected_item)["values"]
            print(refund)
            order_no = refund[0]

            # Prepare the data to update the refund status
            data = {
                "status": "rejected",
                "refund_amount": refund[0]
            }

            # API URL for updating refund status (replace with actual URL)
            url = f"http://127.0.0.1:8000/api/orders/{order_no}/refund/"

            headers = {
                "Authorization": "Token 8a4a2dd557f121b3fd7c3999f59b4604d49069ae",  # Replace <your_token> with actual token
                "Content-Type": "application/json"
            }

            try:
                # Make the PATCH request to the API to update the refund status
                response = requests.put(url, json=data, headers=headers)

                print(response.text)

                if response.status_code == 200:
                    # Update the status in the table
                    self.table.item(selected_item, values=(refund[0], refund[1], refund[2], refund[3], refund[4], 
                                                        refund[5], refund[6], refund[7], "Rejected", refund[9]))
                    print(f"Refund declined for Order No: {order_no}")
                    messagebox.showinfo("Success", f"Refund for Order No {order_no} has been rejected successfully.")
                else:
                    print("Failed to rejected the refund:", response.json())
                    messagebox.showerror("Error", f"Failed to rejected refund for Order No {order_no}.")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while making the API request: {e}")
                messagebox.showerror("Error", "An error occurred while processing the refund. Please try again.")
        else:
            print("No row selected")
            messagebox.showwarning("Selection", "Please select a refund to rejected.")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x500")  # Set window size to fit desktop screen
    RefundScreen(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
