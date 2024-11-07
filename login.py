import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import requests

from token_utils import save_token, get_token
from dashboard_procurement.dashboard import DashboardScreen

TOKEN = get_token()

class LoginScreen(tk.Frame):
    def __init__(self, master=None, on_login_success=None):
        super().__init__(master, bg="grey")  # Outer frame background (grey)
        self.on_login_success = on_login_success  # Function to call on successful login

        # Create a canvas that matches the background to give the illusion of transparency
        self.canvas = tk.Canvas(self, width=500, height=500, bg="grey", highlightthickness=0, bd=0)  # Grey background
        self.canvas.pack(pady=(50, 0))  # Center the canvas with some padding from the top

        # Draw the rounded rectangle as the background for the login elements
        self.round_rectangle(0, 0, 500, 500, radius=100, fill="#397D49")  # Rounded corners for the frame

        # Place the user image above the login text with increased size
        try:
            self.user_image = Image.open("assets/user.png")  # Load the user image
            self.user_image = self.user_image.resize((120, 120), Image.LANCZOS)  # Increased size
            self.user_photo = ImageTk.PhotoImage(self.user_image)

            # Display the user image on the canvas
            self.canvas.create_image(250, 90, image=self.user_photo)  # Center the image

        except FileNotFoundError:
            print("Error: Image file not found. Please check the image path.")

        # Add the "Login" label on the canvas
        self.canvas.create_text(250, 170, text="Admin Munisipyo", font=("Arial", 18), fill="white")  # Adjusted position

        # Create entry frames for username and password with increased spacing
        self.create_entry_with_icon("Username", "assets/user.png", 240)  # Store username entry
        self.create_entry_with_icon("Password", "assets/lock.png", 300, show="*")  # Store password entry

        # Create a rounded green-bordered button
        self.create_rounded_button()

    def create_entry_with_icon(self, placeholder, icon_path, y_position, show=None):
        """Create an entry widget with an icon."""
        # Load the icon image
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((30, 30), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)

        # Create a frame to hold the icon and entry
        entry_frame = tk.Frame(self.canvas, bg="#E0E0E0")
        entry_frame.place(x=125, y=y_position, width=250, height=40)

        # Create the icon label
        icon_label = tk.Label(entry_frame, image=icon_photo, bg="#E0E0E0")
        icon_label.image = icon_photo  # Keep a reference to avoid garbage collection
        icon_label.pack(side=tk.LEFT, padx=5)

        # Create the entry
        entry = tk.Entry(entry_frame, width=18, show=show, bg="#E0E0E0", bd=0, highlightthickness=0,
                         font=("Arial", 16), justify='left')  # Added justify='left'
        entry.insert(0, placeholder)  # Placeholder text
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.restore_placeholder(entry, placeholder))
        entry.pack(side=tk.LEFT, fill=tk.X, padx=5)

        # Store reference to the entry widget
        if placeholder == "Username":
            self.username_entry = entry
        elif placeholder == "Password":
            self.password_entry = entry

    def create_rounded_button(self):
        """Create a button with a rounded background image and place it directly on the canvas."""
        # Create a rounded rectangle image with a yellow background and green border
        btn_width = 200
        btn_height = 50
        radius = 25
        btn_image = Image.new('RGBA', (btn_width, btn_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(btn_image)

        # Set the border outline color to green to match the login frame
        draw.rounded_rectangle([(0, 0), (btn_width, btn_height)], radius=radius, outline="#397D49", width=3, fill="yellow")

        # Convert the image to Tkinter compatible format
        self.button_image = ImageTk.PhotoImage(btn_image)

        # Create a button using the image with rounded corners
        self.login_button = tk.Button(
            self,  # Place the button directly on the canvas (no grey frame)
            image=self.button_image,
            command=self.login,
            text="Login",  # Button text
            compound="center",  # Center the text on top of the image
            font=("Arial", 12, "bold"),  # Text styling
            fg="black",  # Text color
            bd=0,  # Remove button border
            highlightthickness=0,  # No border
            bg="#397D49"  # Set button background to match the green border/frame
        )

        # Place the button at the bottom of the canvas (inside the green frame)
        self.canvas.create_window(250, 450, window=self.login_button)  # Adjusted position

    def login(self):
        # Get the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Ensure both username and password are filled
        if username and password:
            # Define the payload with username and password
            payload = {
                'username': username,
                'password': password
            }

            # Send a POST request to the login endpoint
            try:
                response = requests.post("http://127.0.0.1:8000/api/login/", json=payload)
                
                # Check if login was successful
                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Extract token, user_type, and message from response
                    token = response_data.get("token")
                    user_type = response_data.get("user_type")
                    message = response_data.get("message")
                    
                    # Print login message
                    print(message)

                    print(user_type)
                    # Check if user_type is procurement_admin
                    if user_type == "municipal_admin":
                        self.on_login_success(username)
                        save_token(token=token, username=username)
                    elif user_type == "procurement_admin":
                        for widget in self.master.winfo_children():
                            widget.destroy()
                        
                        # Display the user's information in the header
                        self.master.master.header.create_user_info(username)

                        # Load and display the DashboardScreen
                    
                        dashboard_screen = DashboardScreen(self.master, self.master.master.logout)
                        dashboard_screen.pack(expand=True, fill="both")
                        save_token(token=token, username=username)

                else:
                    print("Login failed! Invalid credentials or server error.")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        else:
            print("Login failed! Please enter valid credentials.")
    def round_rectangle(self, x1, y1, x2, y2, radius=50, **kwargs):
        """Draw a rounded rectangle on the canvas."""
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def clear_placeholder(self, entry, placeholder):
        """Clear the placeholder text when the entry gains focus."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def restore_placeholder(self, entry, placeholder):
        """Restore the placeholder text if the entry is empty when it loses focus."""
        if entry.get() == "":
            entry.insert(0, placeholder)

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = LoginScreen(root)
    login_screen.pack()
    root.mainloop()
