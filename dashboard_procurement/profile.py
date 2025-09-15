import tkinter as tk
from tkinter import ttk
from token_utils import get_username, get_token
import requests

class ProfileScreen(tk.Frame):
    def __init__(self, master, on_logout=None):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.on_logout = on_logout
        self.create_widgets()

    def create_widgets(self):
        # Title label
        tk.Label(self, text="User Profile", font=("Arial", 16, "bold"), bg="lightgrey").pack(pady=20)

        # Create a frame for the profile info with a white background and padding
        profile_frame = tk.Frame(self, bg="white", padx=30, pady=30)
        profile_frame.pack(padx=50, pady=20)

        # Get user data
        self.load_user_data()

    def load_user_data(self):
        """Load user data from the API"""
        from config import API_BASE_URL
        username = get_username()
        token = get_token()

        url = f"{API_BASE_URL}/api/accounts/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {token}'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                accounts = response.json()
                # Find the current user's account
                user_account = next((acc for acc in accounts if acc['username'] == username), None)
                
                if user_account:
                    self.display_user_info(user_account)
                else:
                    tk.Label(self, text="User information not found", fg="red").pack()
            else:
                tk.Label(self, text="Failed to load user information", fg="red").pack()
        except Exception as e:
            tk.Label(self, text=f"Error: {str(e)}", fg="red").pack()

    def display_user_info(self, user_data):
        """Display the user information in a formatted way"""
        # Create a frame for the profile info
        info_frame = tk.Frame(self, bg="white", padx=40, pady=30)
        info_frame.pack(fill="x", padx=50)

        # Style for the labels
        title_style = ("Arial", 12, "bold")
        value_style = ("Arial", 12)
        
        # Create labels for each piece of information
        fields = [
            ("Name", user_data.get('name', 'N/A')),
            ("Username", user_data.get('username', 'N/A')),
            ("Email", user_data.get('email', 'N/A')),
            ("Role", "Procurement Admin"),
            ("Contact", user_data.get('contact', 'N/A')),
            ("Address", user_data.get('address', 'N/A')),
            ("ID Number", user_data.get('id_no', 'N/A')),
            ("Position", user_data.get('position', 'N/A'))
        ]

        # Display each field
        for row, (title, value) in enumerate(fields):
            # Create a frame for each row
            row_frame = tk.Frame(info_frame, bg="white")
            row_frame.pack(fill="x", pady=5)

            # Title label (left)
            tk.Label(row_frame, 
                    text=f"{title}:", 
                    font=title_style,
                    width=15,
                    anchor="e",
                    bg="white").pack(side="left", padx=(0, 10))

            # Value label (right)
            tk.Label(row_frame,
                    text=value,
                    font=value_style,
                    bg="white").pack(side="left")

        # Add some space before the logout button
        tk.Frame(info_frame, height=30, bg="white").pack()

        # Create a frame for the logout button with red background
        logout_button = tk.Button(
            info_frame,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg="#FF4444",  # Red background
            fg="white",    # White text
            activebackground="#CC0000",  # Darker red when clicked
            activeforeground="white",
            padx=30,
            pady=10,
            command=self.on_logout if self.on_logout else self.default_logout
        )
        logout_button.pack(pady=20)

    def default_logout(self):
        """Default logout behavior if no callback is provided"""
        from tkinter import messagebox
        messagebox.showinfo("Logout", "Logout functionality not configured")

# For testing the profile screen independently
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = ProfileScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
