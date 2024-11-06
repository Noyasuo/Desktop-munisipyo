import tkinter as tk
from tkinter import ttk

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

    def populate_table(self):
        """Populate the table with dynamic data (Currently empty)."""
        # This function can later be used to populate the table with data if needed
        pass

# To test the ApprovedScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = ApprovedScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
