import tkinter as tk
from tkinter import messagebox
import requests
from login import TOKEN

class RequestProductScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Main frame to center the content and create a "card" appearance
        card_frame = tk.Frame(self, bg="white", bd=2, relief="groove")
        card_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=320)

        # Title label
        tk.Label(card_frame, text="Request Product", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=(10, 15))

        # Product Name
        tk.Label(card_frame, text="Product Name:", bg="white", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.product_name_entry = tk.Entry(card_frame, width=20, justify="center", relief="solid", bd=1)  # Reduced width
        self.product_name_entry.pack(pady=5, padx=20, fill="x")

        # Quantity
        tk.Label(card_frame, text="Quantity:", bg="white", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.quantity_entry = tk.Entry(card_frame, width=20, justify="center", relief="solid", bd=1)  # Reduced width
        self.quantity_entry.pack(pady=5, padx=20, fill="x")

        # Description
        tk.Label(card_frame, text="Description:", bg="white", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.description_text = tk.Text(card_frame, width=20, height=4, wrap="word", relief="solid", bd=1)  # Reduced width
        self.description_text.pack(pady=5, padx=20, fill="x")

        # Submit button
        submit_button = tk.Button(card_frame, text="Submit Request", command=self.submit_request, bg="#397D49", fg="white", font=("Arial", 10, "bold"))
        submit_button.pack(pady=15)

    def submit_request(self):
        """Handle the submit action."""
        # Get the input values from the fields
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        description = self.description_text.get("1.0", "end-1c")
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }

        # Check if required fields are filled
        if not product_name or not quantity:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        # Prepare data payload for the request
        data = {
            "product_name": product_name,
            "quantity": int(quantity),  # Ensure quantity is an integer
            "description": description
        }

        print(data)

        # Make POST request to API endpoint
        try:
            response = requests.post("http://127.0.0.1:8000/api/orders/", headers=headers, json=data)
            if response.status_code == 201:
                messagebox.showinfo("Request Submitted", "Your product request has been submitted successfully.")

                # Clear fields after submission
                self.product_name_entry.delete(0, "end")
                self.quantity_entry.delete(0, "end")
                self.description_text.delete("1.0", "end")
            else:
                messagebox.showerror("Submission Failed", f"{response.text}")

        except requests.exceptions.RequestException as e:
            # Show error message if request fails
            messagebox.showerror("Submission Failed", f"An error occurred: {e}")

# Testing the RequestProductScreen independently
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = RequestProductScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
