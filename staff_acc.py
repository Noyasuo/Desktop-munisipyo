import tkinter as tk
from tkinter import ttk, messagebox
import requests
from login import TOKEN

class StaffAccScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.create_style()  # Create custom styles
        self.create_widgets()
        self.token = "8a4a2dd557f121b3fd7c3999f59b4604d49069ae" 

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
        # Title label for Staff Accounts
        tk.Label(self, text="Staff Accounts Management", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=20)

        # Frame for the table and scrollbar
        table_frame = tk.Frame(self, bg="lightgrey")  # Set background color for the frame
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Create the Treeview widget for the table
        self.tree = ttk.Treeview(table_frame, columns=("Name", "Email", "Address", "Contact", "ID No.", "Position", "Username", "Password"), show="headings", style="Custom.Treeview")

        # Define the headings and configure their styles
        headings = ["Name", "Email", "Address", "Contact", "ID No.", "Position", "Username", "Password"]
        column_widths = [120, 180, 120, 100, 60, 100, 100, 100]  # Adjusted widths for each column

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
        """Fetch account data from the API and populate the table."""
        url = "http://127.0.0.1:8000/api/accounts/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }

        try:
            response = requests.get(url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                accounts_data = response.json()
                
                # Clear existing entries in the treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insert each account into the treeview
                for account in accounts_data:
                    # Extract values you want to display in the table
                    if account["position"] == "dean" or account["position"] == "head":
                        row = (
                            account["first_name"] + " " + account["last_name"],
                            account["email"],
                            account["address"],
                            account["contact_number"],
                            account["id_number"],
                            account["position"],  # Example field for superuser status
                            account["username"],
                            "********"
                        )
                        self.tree.insert("", "end", values=row)
                
                print("Table populated successfully.")
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def edit_account(self):
        """Edit the selected account with the entire row shown in one dialog."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select an account to edit.")
            return

        # Get current values of the selected row
        item_values = self.tree.item(selected_item)["values"]

        # Create an edit window
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Account")
        edit_window.geometry("400x300")

        # Store new entry widgets to retrieve updated values
        entry_widgets = []

        # Define field names for easy reference
        fields = ["Name", "Email", "Address", "Contact", "ID No.", "Position", "Username", "Password"]

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
            messagebox.showinfo("Success", "Account details updated successfully.")
            edit_window.destroy()

        # Save button with green color
        save_button = tk.Button(edit_window, text="Save", command=save_changes, bg="green", fg="white", font=("Arial", 12), relief="solid", borderwidth=1)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_account(self):
        """Delete the selected account."""
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            messagebox.showinfo("Account Deleted", "The selected account has been deleted.")
        else:
            messagebox.showwarning("No Selection", "Please select an account to delete.")

# To test the StaffAccScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    app = StaffAccScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
