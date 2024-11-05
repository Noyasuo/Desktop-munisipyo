import tkinter as tk
from tkinter import ttk, messagebox

class SupplierAccScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
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
        # Title label for Supplier Accounts
        tk.Label(self, text="Supplier Accounts Management", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=20)

        # Frame for the table and scrollbar
        table_frame = tk.Frame(self, bg="lightgrey")  # Set background color for the frame
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Create the Treeview widget for the table
        self.tree = ttk.Treeview(table_frame, columns=("Name", "Email", "Address", "Valid ID", "Contact", "Business Permit"), show="headings", style="Custom.Treeview")

        # Define the headings and configure their styles
        headings = ["Name", "Email", "Address", "Valid ID", "Contact", "Business Permit"]
        column_widths = [120, 180, 150, 100, 100, 150]  # Adjusted widths for each column

        for col, width in zip(headings, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width)  # Set width for each column

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate the table with example data
        self.populate_table()

        # Buttons for Edit and Delete actions
        button_frame = tk.Frame(self, bg="lightgrey")  # Set background color for button frame
        button_frame.pack(pady=10)

        edit_button = tk.Button(button_frame, text="Edit", command=self.edit_account, bg="green", fg="white", font=("Arial", 12), relief="solid", borderwidth=1)
        edit_button.pack(side="left", padx=10)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_account, bg="red", fg="white", font=("Arial", 12), relief="solid", borderwidth=1)
        delete_button.pack(side="left", padx=10)

    def populate_table(self):
        """Populate the table with example data."""
        example_data = [
            ("Supplier A", "supplierA@example.com", "123 ABC St", "ID12345", "555-1234", "Permit001"),
            ("Supplier B", "supplierB@example.com", "456 DEF St", "ID67890", "555-5678", "Permit002"),
            ("Supplier C", "supplierC@example.com", "789 GHI St", "ID54321", "555-8765", "Permit003"),
        ]

        for item in example_data:
            self.tree.insert("", "end", values=item)

    def edit_account(self):
        """Edit the selected supplier account with the entire row shown in one dialog."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a supplier account to edit.")
            return

        # Get current values of the selected row
        item_values = self.tree.item(selected_item)["values"]

        # Create an edit window
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Supplier Account")
        edit_window.geometry("400x300")

        # Store new entry widgets to retrieve updated values
        entry_widgets = []

        # Define field names for easy reference
        fields = ["Name", "Email", "Address", "Valid ID", "Contact", "Business Permit"]

        # Create entry fields for each column
        for i, field in enumerate(fields):
            tk.Label(edit_window, text=field, font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(edit_window, font=("Arial", 10))
            entry.insert(0, item_values[i])  # Populate with current value
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry_widgets.append(entry)

        # Save changes and update the Treeview item
        def save_changes():
            new_values = [entry.get() for entry in entry_widgets]
            self.tree.item(selected_item, values=new_values)  # Update Treeview with new values
            messagebox.showinfo("Success", "Supplier account details updated successfully.")
            edit_window.destroy()

        # Save button with green color
        save_button = tk.Button(edit_window, text="Save", command=save_changes, bg="green", fg="white", font=("Arial", 12), relief="solid", borderwidth=1)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_account(self):
        """Delete the selected supplier account."""
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            messagebox.showinfo("Account Deleted", "The selected supplier account has been deleted.")
        else:
            messagebox.showwarning("No Selection", "Please select a supplier account to delete.")

# To test the SupplierAccScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    app = SupplierAccScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
