import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox

class InsertCategoryScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="lightgrey")
        self.configure(bg="lightgrey")

        # Create the card frame with padding to move it down a bit
        card_frame = tk.Frame(self, bg="white", padx=20, pady=20, relief="raised", borderwidth=2)
        card_frame.pack(padx=20, pady=(40, 20))  # Add more space at the top to move the card down

        # Title for the Insert Category screen inside the card
        tk.Label(card_frame, text="Insert Category", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

        # Category Name
        self.category_name_entry = self.add_label_and_entry(card_frame, "Category Name:", 1)

        # Description box
        description_label = tk.Label(card_frame, text="Description:", font=("Arial", 14), bg="white", anchor='w')
        description_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.description_box = tk.Text(card_frame, height=4, width=30)
        self.description_box.grid(row=2, column=1, padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(card_frame, text="Insert Category", command=self.submit_category)
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

    def add_label_and_entry(self, frame, label_text, row):
        """Helper method to add a label and entry field."""
        label = tk.Label(frame, text=label_text, font=("Arial", 14), bg="white", anchor='w')
        label.grid(row=row, column=0, padx=10, pady=5, sticky='e')
        entry = tk.Entry(frame, width=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry 

    def submit_category(self):
        from login import TOKEN
        """Handle category submission logic."""
        category_name = self.category_name_entry.get()
        description = self.description_box.get("1.0", tk.END).strip()

        # Check if category name is empty
        if not category_name:
            messagebox.showerror("Error", "Category name is required.")
            return

        # API endpoint and headers
        url = 'http://127.0.0.1:8000/api/category/'
        headers = {
            'Authorization': f'Token {TOKEN}',
            'Content-Type': 'application/json',
        }

        # Prepare the payload
        payload = {
            "name": category_name,
            "description": description
        }

        # Send POST request to create the category
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Category successfully inserted!")
            else:
                messagebox.showerror("Error", f"Failed to insert category: {response.status_code}, {response.json()}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Example of how to run this in a Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Insert Category Screen")
    root.geometry("500x400")  # Adjust window size as needed
    app = InsertCategoryScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
