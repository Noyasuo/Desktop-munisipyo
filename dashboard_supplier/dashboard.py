import tkinter as tk
from PIL import Image, ImageTk
from dashboard_supplier.insert_product import InsertProductScreen
from dashboard_supplier.view_product import ViewProductScreen
from dashboard_supplier.view_order import ViewOrderScreen
from dashboard_supplier.view_payment import ViewPaymentScreen
from dashboard_supplier.refund import RefundScreen
from dashboard_supplier.insert_category import InsertCategoryScreen
from dashboard_supplier.view_category import ViewCategoryScreen

class DashboardScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#f5f5f5")
        
        # Sidebar (menu) frame with a lighter yellow background
        self.menu_frame = tk.Frame(self, bg="#FFEA00", width=200, height=600)  # Brighter yellow
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Content area frame (for dynamic views)
        self.content_frame = tk.Frame(self, bg="#f5f5f5")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Define the menu items and their associated icons
        self.menu_items = [
            ("Dashboard", "dashboard_supplier/assets/dashboard.png", self.show_dashboard),
            ("Products", "dashboard_supplier/assets/products.png", self.toggle_products_buttons),
            ("Categories", "dashboard_supplier/assets/categories.png", self.toggle_categories_buttons),
            ("View Order", "dashboard_supplier/assets/view-order.png", self.show_view_order),
            ("View Payment", "dashboard_supplier/assets/view-payment.png", self.show_view_payment),
            ("Refund", "dashboard_supplier/assets/refund.png", self.show_refund),
            ("Logout", "dashboard_supplier/assets/logout.png", self.show_logout)
        ]

        self.create_menu()

        # Frame for product buttons, initially hidden
        self.product_button_frame = None
        # Frame for categories buttons, initially hidden
        self.categories_button_frame = None

        # Adding dashboard widgets for Products, Categories, and Requests
        self.create_dashboard_widgets()

    def create_menu(self):
        """Creates the vertical sidebar menu."""
        self.menu_item_frame = tk.Frame(self.menu_frame, bg="#FFEA00")  # Brighter yellow
        self.menu_item_frame.pack(pady=20)

        for item, icon_path, command in self.menu_items:
            item_frame = tk.Frame(self.menu_item_frame, bg="#FFEA00")  # Brighter yellow
            item_frame.pack(fill=tk.X, pady=10)

            # Load and resize the icon
            try:
                icon = Image.open(icon_path)
                icon = icon.resize((30, 30), Image.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon)
            except FileNotFoundError:
                print(f"Error: Icon file '{icon_path}' not found.")
                icon_photo = None

            if icon_photo:
                icon_label = tk.Label(item_frame, image=icon_photo, bg="#FFEA00")  # Brighter yellow
                icon_label.image = icon_photo
                icon_label.pack(side=tk.LEFT, padx=10)

            text_label = tk.Label(item_frame, text=item, font=("Arial", 14), fg="black", bg="#FFEA00")  # Brighter yellow
            text_label.pack(side=tk.LEFT, padx=10)

            text_label.bind("<Button-1>", lambda e, cmd=command: cmd())

            if item == "Dashboard":
                self.dashboard_label = text_label  # Store reference to update later
            elif item == "Products":
                self.product_label_frame = item_frame
            elif item == "Categories":
                self.categories_label_frame = item_frame

    def create_dashboard_widgets(self):
        """Adds the 3 main widgets (Products, Categories, Requests) to the dashboard screen."""
        # Clear any existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Dashboard main widgets frame
        widgets_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
        widgets_frame.pack(pady=20)

        # Create the Products widget (set same size for all widgets)
        self.create_widget_button(widgets_frame, "View Products", "dashboard_supplier/assets/products.png", 0, "view_product")

        # Create the Categories widget
        self.create_widget_button(widgets_frame, "View Categories", "dashboard_supplier/assets/categories.png", 1, "view_categories")

        # Create the Requests widget
        self.create_widget_button(widgets_frame, "View Requests", "dashboard_supplier/assets/products.png", 2, "view_order")

    def create_widget_button(self, parent_frame, text, icon_path, column, route_name):
        """Helper function to create a widget button with an icon and text with equal sizes."""
        widget_frame = tk.Frame(parent_frame, bg="lightgray", relief=tk.RAISED, bd=2, width=200, height=200)
        widget_frame.grid(row=0, column=column, padx=20, pady=20)

        widget_frame.grid_propagate(False)  # Prevent the frame from resizing to fit content

        # Load and resize the icon
        try:
            icon = Image.open(icon_path)
            icon = icon.resize((50, 50), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon)
        except FileNotFoundError:
            print(f"Error: Icon file '{icon_path}' not found.")
            icon_photo = None

        if icon_photo:
            icon_label = tk.Label(widget_frame, image=icon_photo, bg="lightgray")
            icon_label.image = icon_photo
            icon_label.pack(pady=10)

        text_label = tk.Label(widget_frame, text=text, font=("Arial", 14), fg="black", bg="lightgray")
        text_label.pack()

        # Bind the click event to the appropriate routing function
        text_label.bind("<Button-1>", lambda e, name=route_name: self.route_view(name))

    def route_view(self, view_name):
        """Routes to the appropriate view based on the widget clicked."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if view_name == "view_product":
            ViewProductScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif view_name == "view_categories":
            ViewCategoryScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif view_name == "view_order":
            ViewOrderScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def toggle_products_buttons(self):
        """Toggle 'Insert Product' and 'View Product' buttons."""
        if self.product_button_frame:
            self.product_button_frame.destroy()
            self.product_button_frame = None
        else:
            self.product_button_frame = tk.Frame(self, bg="lightgray")

            insert_button = tk.Button(self.product_button_frame, text="Insert Product", 
                                      command=self.show_insert_product, bg="lightgray")
            view_button = tk.Button(self.product_button_frame, text="View Product", 
                                    command=self.show_view_product, bg="lightgray")

            insert_button.pack(fill=tk.X, pady=2)
            view_button.pack(fill=tk.X, pady=2)

            self.product_button_frame.place(in_=self.product_label_frame, relx=1.05, rely=0)

    def toggle_categories_buttons(self):
        """Toggle 'Insert Categories' and 'View Categories' buttons."""
        if self.categories_button_frame:
            self.categories_button_frame.destroy()
            self.categories_button_frame = None
        else:
            self.categories_button_frame = tk.Frame(self, bg="lightgray")

            insert_button = tk.Button(self.categories_button_frame, text="Insert Categories", 
                                      command=self.show_insert_categories, bg="lightgray")
            view_button = tk.Button(self.categories_button_frame, text="View Categories", 
                                    command=self.show_view_categories, bg="lightgray")

            insert_button.pack(fill=tk.X, pady=2)
            view_button.pack(fill=tk.X, pady=2)

            self.categories_button_frame.place(in_=self.categories_label_frame, relx=1.05, rely=0)

    def show_insert_product(self):
        """Switch content to Insert Product view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        InsertProductScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def show_view_product(self):
        """Switch content to View Product view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ViewProductScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def show_insert_categories(self):
        """Switch content to Insert Categories view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        InsertCategoryScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def show_view_categories(self):
        """Switch content to View Categories view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ViewCategoryScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def show_view_order(self):
        """Switch content to View Order view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ViewOrderScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def show_view_payment(self):
        """Switch content to View Payment view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ViewPaymentScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def show_refund(self):
        """Switch content to Refund view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        RefundScreen(self.content_frame).pack(fill=tk.BOTH, expand=True)

    def show_logout(self):
        """Implement logout functionality here."""
        pass

    def show_dashboard(self):
        """Show the dashboard view."""
        self.create_dashboard_widgets()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Dashboard")
    app = DashboardScreen(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
