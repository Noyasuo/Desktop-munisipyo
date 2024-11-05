import tkinter as tk

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

        # Sidebar menu items
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Request Item", self.show_request_item),
            ("Staff Acc", self.show_staff_accounts),
            ("Supplier Acc", self.show_supplier_accounts),
            ("Supplier Sale", self.show_supplier_sale),
            ("Logout", self.on_logout)
        ]

        for item, command in menu_items:
            btn = tk.Button(self.sidebar_frame, text=item, command=command)
            btn.pack(fill='x', padx=10, pady=3)

        # Main content area
        self.content_frame = tk.Frame(self, bg="lightgrey")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Initialize with the dashboard view
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Dashboard Screen", bg="lightgrey", font=("Arial", 16)).pack(expand=True)

    def show_request_item(self):
        self.clear_content_frame()
        try:
            from request_item import RequestItemScreen  # Import the screen from request_item.py
            request_item_screen = RequestItemScreen(self.content_frame)
            request_item_screen.pack(fill="both", expand=True)
        except ImportError:
            tk.Label(self.content_frame, text="Error: request_item.py not found.", bg="lightgrey", font=("Arial", 16)).pack(expand=True)

    def show_staff_accounts(self):
        self.clear_content_frame()
        try:
            from staff_acc import StaffAccScreen  # Import the screen from staff_acc.py
            staff_acc_screen = StaffAccScreen(self.content_frame)
            staff_acc_screen.pack(fill="both", expand=True)
        except ImportError:
            tk.Label(self.content_frame, text="Error: staff_acc.py not found.", bg="lightgrey", font=("Arial", 16)).pack(expand=True)

    def show_supplier_accounts(self):
        self.clear_content_frame()
        try:
            from supplier_acc import SupplierAccScreen  # Import the screen from supplier_acc.py
            supplier_acc_screen = SupplierAccScreen(self.content_frame)
            supplier_acc_screen.pack(fill="both", expand=True)
        except ImportError:
            tk.Label(self.content_frame, text="Error: supplier_acc.py not found.", bg="lightgrey", font=("Arial", 16)).pack(expand=True)

    def show_supplier_sale(self):
        self.clear_content_frame()
        try:
            from supplier_sale import SupplierSaleScreen  # Import the screen from supplier_sale.py
            supplier_sale_screen = SupplierSaleScreen(self.content_frame)
            supplier_sale_screen.pack(fill="both", expand=True)
        except ImportError:
            tk.Label(self.content_frame, text="Error: supplier_sale.py not found.", bg="lightgrey", font=("Arial", 16)).pack(expand=True)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = DashboardScreen(root, lambda: print("Logged out!"))
    app.pack(fill="both", expand=True)
    root.mainloop()
