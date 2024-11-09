import tkinter as tk
from tkinter import ttk, messagebox
import requests


class ViewCategoryScreen(tk.Frame):
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
        tk.Label(self, text="View Categories", font=("Arial", 16), bg="lightgrey").pack(pady=20)

        # Create a frame for the table
        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview widget) with custom style
        self.category_tree = ttk.Treeview(
            table_frame,
            style="Custom.Treeview",
            columns=("Category ID", "Category Title", "Category Description"),
            show="headings"
        )

        # Define headings and column widths
        self.category_tree.heading("Category ID", text="Category ID")
        self.category_tree.heading("Category Title", text="Category Title")
        self.category_tree.heading("Category Description", text="Category Description")

        self.category_tree.column("Category ID", width=100, anchor=tk.CENTER)
        self.category_tree.column("Category Title", width=150, anchor=tk.W)
        self.category_tree.column("Category Description", width=200, anchor=tk.W)

        # Add sample data to the table
        self.populate_table()

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the table into the frame
        self.category_tree.pack(fill="both", expand=True)

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
        """Populates the table with data from the API."""
        # API URL and headers
        url = 'http://127.0.0.1:8000/api/category/'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }
        
        # Fetch data from the API
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Iterate over the data and insert it into the table
            for item in data:
                row = (item['id'], item['name'], item['description'])
                self.category_tree.insert("", "end", values=row)
        else:
            print(f"Error fetching data: {response.status_code}")

    def on_edit_button_click(self):
        """Handle the edit button click."""
        selected_item = self.category_tree.selection()
        if selected_item:
            # Get the values of the selected row
            category_id = self.category_tree.item(selected_item)["values"][0]
            title = self.category_tree.item(selected_item)["values"][1]
            description = self.category_tree.item(selected_item)["values"][2]

            # Create a pop-up window (dialog) for editing
            self.open_edit_dialog(selected_item, category_id, title, description)
        else:
            messagebox.showwarning("Selection Error", "Please select a category to edit.")

    def open_edit_dialog(self, selected_item, category_id, title, description):
        """Open a dialog for editing the category details."""
        # Create a new window for editing
        edit_window = tk.Toplevel(self)
        edit_window.geometry("400x300")
        edit_window.title(f"Edit Category ID {category_id}")

        # Fields to edit category information
        tk.Label(edit_window, text="Category Title").pack(pady=5)
        title_entry = tk.Entry(edit_window, font=("Arial", 12))
        title_entry.insert(0, title)
        title_entry.pack(pady=5)

        tk.Label(edit_window, text="Category Description").pack(pady=5)
        description_entry = tk.Entry(edit_window, font=("Arial", 12))
        description_entry.insert(0, description)
        description_entry.pack(pady=5)

        # Save button to update the category details
        def save_changes():
            new_title = title_entry.get()
            new_description = description_entry.get()

            # Update the selected category data in the table
            self.category_tree.item(selected_item, values=(category_id, new_title, new_description))
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save Changes", font=("Arial", 12), bg="#4CAF50", fg="white", command=save_changes)
        save_button.pack(pady=10)

        # Cancel button to close the dialog
        cancel_button = tk.Button(edit_window, text="Cancel", font=("Arial", 12), bg="#F44336", fg="white", command=edit_window.destroy)
        cancel_button.pack(pady=10)

    def on_delete_button_click(self):
        """Handle the delete button click."""
        selected_item = self.category_tree.selection()
        if selected_item:
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this category?")
            if confirm:
                self.category_tree.delete(selected_item)
        else:
            messagebox.showwarning("Selection Error", "Please select a category to delete.")

# To test the ViewCategoryScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    app = ViewCategoryScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
