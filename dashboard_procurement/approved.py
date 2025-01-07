import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
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
        self.tree = ttk.Treeview(table_frame, columns=("Name", "Email", "Request Date", "Quantity", "Item"), show="headings", style="Custom.Treeview")

        # Define the headings and configure their styles
        headings = ["Name", "Email", "Request Date", "Quantity", "Item"]
        column_widths = [120, 150, 120, 100, 150]  # Adjusted widths for each column

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

        # Bind row selection to enable the dispatch button
        self.tree.bind("<ButtonRelease-1>", self.on_row_selected)

        # Action frame for the dispatch button
        self.action_frame = tk.Frame(self, bg="lightgrey")
        self.action_frame.pack(pady=10)

        # Dispatch button
        self.dispatch_button = tk.Button(self.action_frame, text="Dispatch", command=self.dispatch_request, state="disabled", bg="blue", fg="white")
        self.dispatch_button.grid(row=0, column=0, padx=10)

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
                    if order['final_status'] == 'approved':
                        # Extract relevant data from the order object
                        user_name = order['user']['username']  # Assuming 'user' is an ID or object, you can modify this to fetch user details
                        user_email = order['user']['email']  # Same as above, replace with actual user email if nested
                        request_date = order['request_date']
                        quantity = order['quantity']
                        # Assuming product is an array (multiple products in an order)
                        item_names = ', '.join([product['title'] for product in order['product']])

                        # Insert data into the table
                        self.tree.insert("", "end", values=(user_name, user_email, request_date, quantity, item_names))
            else:
                # If the request fails, show an error message
                messagebox.showerror("Error", "Failed to retrieve orders data.")
        except Exception as e:
            # If any exception occurs, show an error message
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_row_selected(self, event):
        """Enables the Dispatch button when a row is selected."""
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row_id = selected_item[0]
            # Enable the dispatch button
            self.dispatch_button.config(state="normal")

    def dispatch_request(self):
        """Dispatch the selected request."""
        selected_item = self.tree.selection()
        if selected_item:
            # Get the selected item values
            item_values = self.tree.item(selected_item)['values']
            user_name, user_email, request_date, quantity, item_names = item_values

            # Create a frame for dispatch details
            dispatch_frame = tk.Frame(self, bg="lightgrey")
            dispatch_frame.pack(pady=20)

            # Create and place labels and entry widgets for each field
            fields = ["Name", "Email", "Request Date", "Quantity", "Item"]
            values = [user_name, user_email, request_date, quantity, item_names]
            entries = {}

            for i, (field, value) in enumerate(zip(fields, values)):
                tk.Label(dispatch_frame, text=field, bg="lightgrey").grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(dispatch_frame)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, value)
                entries[field] = entry

            # Confirm button to finalize the dispatch
            confirm_button = tk.Button(dispatch_frame, text="Confirm", command=lambda: self.confirm_dispatch(dispatch_frame, selected_item))
            confirm_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def confirm_dispatch(self, frame, selected_item):
        """Confirm the dispatch and close the frame."""
        # Handle the dispatch logic here
        print(f"Dispatching request for item: {self.tree.item(selected_item)['values']}")
        messagebox.showinfo("Dispatch", "The selected request has been dispatched successfully.")
        # Optionally, update the status in the table or remove the dispatched item
        self.tree.delete(selected_item)
        frame.destroy()

# To test the ApprovedScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = ApprovedScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()