import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
from login import TOKEN

class RequestScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Requests", font=("Arial", 16), bg="lightgrey").pack(pady=20)
        
        # Create a frame for the table
        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview widget) with custom style
        self.table = ttk.Treeview(
            table_frame,
            columns=("order_id", "user_name", "user_email", "request_date", "quantity", "item", "status"),
            show="headings"
        )

        # Define headings and column widths
        self.table.heading("order_id", text="Order ID")
        self.table.heading("user_name", text="User Name")
        self.table.heading("user_email", text="User Email")
        self.table.heading("request_date", text="Request Date")
        self.table.heading("quantity", text="Quantity")
        self.table.heading("item", text="Item")
        self.table.heading("status", text="Status")
        
        self.table.column("order_id", width=120)
        self.table.column("user_name", width=120)
        self.table.column("user_email", width=180)
        self.table.column("request_date", width=100)
        self.table.column("quantity", width=70, anchor="center")
        self.table.column("item", width=180)
        self.table.column("status", width=100, anchor="center")

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the table into the frame
        self.table.pack(fill="both", expand=True)

        # Bind row selection to display approval/decline buttons
        self.table.bind("<ButtonRelease-1>", self.on_row_selected)

        # Action frame for the approval and decline buttons
        self.action_frame = tk.Frame(self, bg="lightgrey")
        self.action_frame.pack(pady=10)

        # Approve button
        self.approve_button = tk.Button(self.action_frame, text="Approve", command=self.approve_request, state="disabled", bg="green", fg="white")
        self.approve_button.grid(row=0, column=0, padx=10)

        # Decline button
        self.decline_button = tk.Button(self.action_frame, text="Decline", command=self.decline_request, state="disabled", bg="red", fg="white")
        self.decline_button.grid(row=0, column=1, padx=10)

        # Fetching data from API
        self.populate_table()

    def populate_table(self):
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
                    # Extract relevant data from the order object
                    if not order['status'] == 'pending':
                        continue
                    user_name = order['user']['username']  # Assuming 'user' is an ID or object, you can modify this to fetch user details
                    user_email = order['user']['email']  # Same as above, replace with actual user email if nested
                    request_date = order['request_date']
                    quantity = order['quantity']
                    status = order['status']
                    order_id = order['id']
                    # Assuming product is an array (multiple products in an order)
                    item_names = ', '.join([product['title'] for product in order['product']])

                    # Insert data into the table
                    self.table.insert("", "end", values=(order_id, user_name, user_email, request_date, quantity, item_names, status))
            else:
                # If the request fails, show an error message
                messagebox.showerror("Error", "Failed to retrieve orders data.")
        except Exception as e:
            # If any exception occurs, show an error message
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_row_selected(self, event):
        """Enables the Approve and Decline buttons when a row is selected."""
        selected_item = self.table.selection()
        if selected_item:
            self.selected_row_id = selected_item[0]
            # Enable the action buttons
            self.approve_button.config(state="normal")
            self.decline_button.config(state="normal")

    def approve_request(self):
        """Approve the selected request."""
        selected_item = self.table.selection()
        if selected_item:
            item_data = self.table.item(selected_item)["values"]
            order_id = item_data[0]  # Assuming the first column is the order ID

            url = f"http://52.62.183.28/api/order/{order_id}/"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Token {TOKEN}'
            }
            data = {
                "status": "approved",
                "final_status": "approved"
            }

            try:
                response = requests.put(url, headers=headers, json=data)
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Order approved successfully.")
                    # Optionally, refresh the table or update the UI
                else:
                    messagebox.showerror("Error", f"Failed to approve order: {response.status_code}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def decline_request(self):
        """Decline the selected request."""
        # Prompt for an optional comment
        comment = simpledialog.askstring("Decline Request", "Reason for decline:")
        self.update_status("declined", comment)

    def update_status(self, status, comment=None):
        """Updates the status of the selected row."""
        selected_item = self.table.selection()
        if selected_item:
            # Update the status in the table
            self.table.set(selected_item, column="status", value=status)
            # Optionally handle the comment (e.g., send it to the server or log it)
            if comment:
                print(f"Comment for declined request: {comment}")
            # Disable the action buttons
            self.approve_button.config(state="disabled")
            self.decline_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = RequestScreen(root)
    app.pack(fill="both", expand=True)
    root.mainloop()