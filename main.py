import tkinter as tk
from PIL import Image, ImageTk
from login import LoginScreen  # Ensure LoginScreen is implemented and takes a callback for login success

class Header(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#397D49")
        self.pack(side="top", fill="x")
        self.pack_propagate(False)
        self.config(height=80)

        # Load and display the logo image
        try:
            self.logo_image = Image.open("assets/logo.png")
            self.logo_image = self.logo_image.resize((60, 60), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self, image=self.logo_photo, bg="#397D49")
            self.logo_label.pack(side="left", padx=10, pady=10)
        except FileNotFoundError:
            print("Error: Logo image file not found. Please check the image path.")

        # School name label
        self.school_label = tk.Label(self, text="Colegio de Montalban", font=("Arial", 16), bg="#397D49", fg="white")
        self.school_label.pack(side="left", padx=10, pady=10)

        self.user_frame = None  # Placeholder for user info frame

    def create_user_info(self, username):
        """Displays user information in the header."""
        self.user_frame = tk.Frame(self, bg="#FFD700")
        self.user_frame.pack(side="right", padx=10)

        try:
            self.user_icon_image = Image.open("assets/user.png")
            self.user_icon_image = self.user_icon_image.resize((20, 20), Image.LANCZOS)
            self.user_icon_photo = ImageTk.PhotoImage(self.user_icon_image)
            self.user_icon_label = tk.Label(self.user_frame, image=self.user_icon_photo, bg="#FFD700")
            self.user_icon_label.pack(side="left", padx=(5, 2))
        except FileNotFoundError:
            print("Error: User icon image file not found. Please check the image path.")

        # Username display
        self.user_box = tk.Label(self.user_frame, text=username, bg="#FFD700", fg="black", font=("Arial", 12), height=2)
        self.user_box.pack(side="left", padx=5)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Desktop Application")
        self.geometry("800x600")
        self.configure(bg="grey")
        self.state('zoomed')

        # Header with logo and title
        self.header = Header(self)
        self.header.pack(side="top", fill="x")

        # Frame to hold the main content (either login or dashboard)
        self.content_frame = tk.Frame(self, bg="grey")
        self.content_frame.pack(expand=True, fill="both")

        # Start with the login screen
        self.show_login_screen()

    def show_login_screen(self):
        """Displays the login screen."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        login_screen = LoginScreen(self.content_frame, self.on_login_success)
        login_screen.pack(pady=20)

    def on_login_success(self, username):
        """Handles successful login by showing the dashboard and updating the header."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Display the user's information in the header
        self.header.create_user_info(username)

        # Load and display the DashboardScreen
        from dashboard import DashboardScreen  # Import inside function to avoid circular imports
        dashboard_screen = DashboardScreen(self.content_frame, self.logout)
        dashboard_screen.pack(expand=True, fill="both")

    def logout(self):
        """Logs the user out by returning to the login screen and clearing user info."""
        if self.header.user_frame:
            self.header.user_frame.destroy()
            self.header.user_frame = None
        self.show_login_screen()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
