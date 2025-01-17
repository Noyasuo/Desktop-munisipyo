import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from .list import ListScreen  # Import ListScreen from list.py
from .reports import ReportsScreen  # Import ReportsScreen from reports.py

class DashboardScreen(tk.Frame):
    def __init__(self, master, on_logout):
        super().__init__(master)
        self.master = master
        self.on_logout = on_logout
        self.create_widgets()

    def create_widgets(self):
        # Sidebar frame with dark yellow background
        self.sidebar_frame = tk.Frame(self, bg="#FFEA00")
        self.sidebar_frame.pack(side="left", fill="y")

        # Spacer frame to adjust the position of the menu items
        spacer = tk.Frame(self.sidebar_frame, height=30, bg="#FFEA00")
        spacer.pack()

        # Menu items for the sidebar
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("List", self.show_list),
            ("Accounts", self.show_staff_accounts),
            ("Inventory", self.show_inventory),
            ("Reports", self.show_reports),  # Added Reports menu item
            ("Logout", self.on_logout)
        ]

        for item, command in menu_items:
            btn = tk.Button(self.sidebar_frame, text=item, command=command)
            btn.pack(fill='x', padx=10, pady=3)

        # Main content area with background image
        self.content_frame = tk.Frame(self, bg="lightgrey")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Load and display the background image
        self.canvas = tk.Canvas(self.content_frame, bg="lightgrey")
        self.canvas.pack(fill="both", expand=True)
        image_path = "assets/home.png"
        if os.path.exists(image_path):
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((self.master.winfo_width(), self.master.winfo_height()), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        else:
            self.canvas.create_text(400, 300, text="Background image not found", font=("Arial", 24), fill="red")

        # Initialize with the dashboard view
        self.show_dashboard()

    def show_dashboard(self):
        """Displays the default dashboard view with four clickable widgets."""
        self.clear_content_frame()

        # Centering frame for the widgets
        center_frame = tk.Frame(self.content_frame, bg="lightgrey")
        center_frame.pack(pady=20, expand=True)

        # Widgets for Request, Approved, Declined, and Dispatched with routing functionality
        widget_data = [
            ("Request", "This is the request widget", self.show_request),
            ("Approved", "This is the approved widget", self.show_approved),
            ("Declined", "This is the declined widget", self.show_declined),
            ("Dispatched", "This is the dispatched widget", self.show_dispatched)  # Added Dispatched widget
        ]

        for title, description, command in widget_data:
            widget = tk.Frame(center_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
            widget.pack(side="left", padx=10, pady=10)
            tk.Label(widget, text=title, font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 5))
            tk.Label(widget, text=description, bg="white").pack()
            widget.bind("<Button-1>", lambda e, cmd=command: cmd())

    def show_request(self):
        from .request import RequestScreen
        self.clear_content_frame()
        request_screen = RequestScreen(self.content_frame)
        request_screen.pack(fill="both", expand=True)

    def show_approved(self):
        from .approved import ApprovedScreen
        self.clear_content_frame()
        approved_screen = ApprovedScreen(self.content_frame)
        approved_screen.pack(fill="both", expand=True)

    def show_declined(self):
        from .disapproved import DisapprovedScreen
        self.clear_content_frame()
        declined_screen = DisapprovedScreen(self.content_frame)
        declined_screen.pack(fill="both", expand=True)

    def show_dispatched(self):
        from .dispatched import DispatchedScreen
        self.clear_content_frame()
        dispatched_screen = DispatchedScreen(self.content_frame)
        dispatched_screen.pack(fill="both", expand=True)

    def show_list(self):
        self.clear_content_frame()
        list_screen = ListScreen(self.content_frame)
        list_screen.pack(fill="both", expand=True)

    def show_staff_accounts(self):
        from .staffacc import StaffAccountsScreen
        self.clear_content_frame()
        staff_accounts_screen = StaffAccountsScreen(self.content_frame)
        staff_accounts_screen.pack(fill="both", expand=True)

    def show_inventory(self):
        """Displays the Inventory screen with 'Insert Inventory' and 'View Inventory' as widgets."""
        self.clear_content_frame()

        # Centering frame for the inventory widgets
        inventory_frame = tk.Frame(self.content_frame, bg="lightgrey")
        inventory_frame.pack(pady=20, expand=True)

        # Inventory widgets data
        inventory_widgets = [
            ("Insert Inventory", "Insert new inventory items", self.insert_inventory),
            ("View Inventory", "View existing inventory items", self.view_inventory)
        ]

        for title, description, command in inventory_widgets:
            widget = tk.Frame(inventory_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
            widget.pack(side="left", padx=10, pady=10)
            tk.Label(widget, text=title, font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 5))
            tk.Label(widget, text=description, bg="white").pack()
            widget.bind("<Button-1>", lambda e, cmd=command: cmd())

    def insert_inventory(self):
        from .insert_inventory import InsertInventoryScreen
        self.clear_content_frame()
        insert_inventory_screen = InsertInventoryScreen(self.content_frame)
        insert_inventory_screen.pack(fill="both", expand=True)

    def view_inventory(self):
        from .view_inventory import ViewInventoryScreen
        self.clear_content_frame()
        view_inventory_screen = ViewInventoryScreen(self.content_frame)
        view_inventory_screen.pack(fill="both", expand=True)

    def show_reports(self):
        """Displays the Reports screen."""
        self.clear_content_frame()
        reports_screen = ReportsScreen(self.content_frame)
        reports_screen.pack(fill="both", expand=True)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = DashboardScreen(root, lambda: print("Logged out!"))
    app.pack(fill="both", expand=True)
    root.mainloop()