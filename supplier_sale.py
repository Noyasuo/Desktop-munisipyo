import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

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
        """Populate the table with example merchandise data."""
        # Example merchandise data (You can replace this with dynamic data from your database or API)
        example_data = [
            ("Product A", "path_to_image_A.png", "Product A", "Description of Product A", "Category 1", "$20", "50"),
            ("Product B", "path_to_image_B.png", "Product B", "Description of Product B", "Category 2", "$25", "30"),
            ("Product C", "path_to_image_C.png", "Product C", "Description of Product C", "Category 3", "$30", "20"),
        ]

        for item in example_data:
            name, img_path, product, description, category, price, quantity = item

            # Load image using PIL (Python Imaging Library)
            try:
                img = Image.open(img_path)
                img = img.resize((50, 50))  # Resize the image to fit in the table
                img = ImageTk.PhotoImage(img)
            except Exception as e:
                img = None
                print(f"Error loading image: {e}")

            # Insert the merchandise data into the table
            self.tree.insert("", "end", values=(name, img, product, description, category, price, quantity))

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
