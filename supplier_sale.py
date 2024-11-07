import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
from login import TOKEN


class SupplierSaleScreen(tk.Frame):
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
        # Title label for Supplier Sale
        tk.Label(self, text="Supplier Merchandise Display", font=("Arial", 16, "bold")).pack(pady=20)

        # Frame for the table and scrollbar
        table_frame = tk.Frame(self)  # Set background color for the frame
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Create the Treeview widget for the table
        self.tree = ttk.Treeview(table_frame, columns=("Name", "Image", "Product", "Description", "Category", "Price", "Quantity"), show="headings", style="Custom.Treeview")

        # Define the headings and configure their styles
        headings = ["Name", "Image", "Product", "Description", "Category", "Price", "Quantity"]
        column_widths = [120, 100, 150, 200, 100, 100, 80]  # Adjusted widths for each column

        for col, width in zip(headings, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width)  # Set width for each column

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate the table with example merchandise data
        self.populate_table()

    def populate_table(self):
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
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insert each product into the table
                for product in products_data:
                    name = product["title"]
                    img_path = product["image"]  # Assuming you want to display the image (could be null)
                    description = product["description"]
                    category = product["category"]["name"]  # Category name from nested JSON
                    price = f"${product['price']}"
                    quantity = product["stock"]
                    
                    # Handle image (if available)
                    img = None
                    if img_path:
                        try:
                            img = Image.open(img_path)  # Open the image if the path is available
                            img = img.resize((50, 50))  # Resize the image to fit in the table
                            img = ImageTk.PhotoImage(img)
                        except Exception as e:
                            print(f"Error loading image: {e}")
                    
                    # Insert the product data into the table
                    self.tree.insert("", "end", values=(name, img, name, description, category, price, quantity))
                
                print("Table populated successfully.")
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def on_item_selected(self, event):
        """Handle item selection in the Treeview."""
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)["values"]
            messagebox.showinfo("Item Selected", f"You selected: {item_values[2]}")

# To test the SupplierSaleScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = SupplierSaleScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
