import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk

import requests


class ViewProductScreen(tk.Frame):
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
        tk.Label(self, text="View Products", font=("Arial", 16), bg="lightgrey").pack(pady=20)

        # Create a frame for the table
        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview widget) with custom style
        self.table = ttk.Treeview(
            table_frame,
            style="Custom.Treeview",
            columns=("Product ID", "Product Title", "Product Price", "Product Keyword", "Product Description"),
            show="headings"
        )

        # Define headings and column widths
        self.table.heading("Product ID", text="Product ID")
        self.table.heading("Product Title", text="Product Title")
        self.table.heading("Product Price", text="Product Price")
        self.table.heading("Product Keyword", text="Product Keyword")
        self.table.heading("Product Description", text="Product Description")

        self.table.column("Product ID", width=100, anchor=tk.CENTER)
        self.table.column("Product Title", width=150, anchor=tk.W)
        self.table.column("Product Price", width=120, anchor=tk.CENTER)
        self.table.column("Product Keyword", width=150, anchor=tk.CENTER)
        self.table.column("Product Description", width=180, anchor=tk.CENTER)

        # Add sample data to the table
        self.populate_table()

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the table into the frame
        self.table.pack(fill="both", expand=True)

        # Action buttons below the table (Edit and Delete buttons)
        action_button_frame = tk.Frame(self, bg="lightgrey")
        action_button_frame.pack(pady=20)

        # Edit button (Yellow)
        self.edit_button = tk.Button(
            action_button_frame,
            text="Edit",
            font=("Arial", 14),
            bg="#FFEB3B",  # Yellow background color
            fg="black",    # Black text color
            command=self.on_edit_button_click
        )
        self.edit_button.pack(side="left", padx=10)

        # Delete button (Red)
        self.delete_button = tk.Button(
            action_button_frame,
            text="Delete",
            font=("Arial", 14),
            bg="#F44336",  # Red background color
            fg="white",    # White text color
            command=self.on_delete_button_click
        )
        self.delete_button.pack(side="left", padx=10)

    def populate_table(self):
        from login import TOKEN

        """Fetch product data from the API and populate the table."""
        url = "http://127.0.0.1:8000/api/products/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }

        try:
            response = requests.get(url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                products_data = response.json()
                
                # Clear existing entries in the table
                for item in self.table.get_children():
                    self.table.delete(item)

                # Insert each product into the table
                for product in products_data:
                    name = product["id"]
                    img_path = product["title"]  # Assuming you want to display the image (could be null)
                    description = product["price"]
                    category = product["category"]["name"] + product["title"]  # Category name from nested JSON
                    price = f"${product['price']}"
                    
                    
                    # Insert the product data into the table
                    self.table.insert("", "end", values=(name, img_path,  name, description, category, price))
                
                print("Table populated successfully.")
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def on_edit_button_click(self):
        """Handle the edit button click."""
        selected_item = self.table.selection()
        if selected_item:
            # Get the values of the selected row
            product_id = self.table.item(selected_item)["values"][0]
            title = self.table.item(selected_item)["values"][1]
            price = self.table.item(selected_item)["values"][2]
            keyword = self.table.item(selected_item)["values"][3]
            date = self.table.item(selected_item)["values"][4]

            # Create a pop-up window (dialog) for editing
            self.open_edit_dialog(selected_item, product_id, title, price, keyword, date)
        else:
            messagebox.showwarning("Selection Error", "Please select a product to edit.")

    def open_edit_dialog(self, selected_item, product_id, title, price, keyword, date):
        """Open a dialog for editing the product details."""
        # Create a new window for editing
        edit_window = tk.Toplevel(self)
        edit_window.geometry("400x300")
        edit_window.title(f"Edit Product ID {product_id}")

        # Fields to edit product information
        tk.Label(edit_window, text="Product Title").pack(pady=5)
        title_entry = tk.Entry(edit_window, font=("Arial", 12))
        title_entry.insert(0, title)
        title_entry.pack(pady=5)

        tk.Label(edit_window, text="Product Price").pack(pady=5)
        price_entry = tk.Entry(edit_window, font=("Arial", 12))
        price_entry.insert(0, price)
        price_entry.pack(pady=5)

        tk.Label(edit_window, text="Product Keyword").pack(pady=5)
        keyword_entry = tk.Entry(edit_window, font=("Arial", 12))
        keyword_entry.insert(0, keyword)
        keyword_entry.pack(pady=5)

        tk.Label(edit_window, text="Product Date").pack(pady=5)
        date_entry = tk.Entry(edit_window, font=("Arial", 12))
        date_entry.insert(0, date)
        date_entry.pack(pady=5)

        # Save button to update the product details
        def save_changes():
            new_title = title_entry.get()
            new_price = price_entry.get()
            new_keyword = keyword_entry.get()
            new_date = date_entry.get()

            # Update the selected product data in the table
            self.table.item(selected_item, values=(product_id, new_title, new_price, new_keyword, new_date))
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save Changes", font=("Arial", 12), bg="#4CAF50", fg="white", command=save_changes)
        save_button.pack(pady=10)

        # Cancel button to close the dialog
        cancel_button = tk.Button(edit_window, text="Cancel", font=("Arial", 12), bg="#F44336", fg="white", command=edit_window.destroy)
        cancel_button.pack(pady=10)

    def on_delete_button_click(self):
        """Handle the delete button click."""
        selected_item = self.table.selection()
        if selected_item:
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this product?")
            if confirm:
                self.table.delete(selected_item)
        else:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")

# To test the ViewProductScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    app = ViewProductScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
