import tkinter as tk
from tkinter import ttk

class RequestItemScreen(tk.Frame):
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
        tk.Label(self, text="Request Items", font=("Arial", 16), bg="lightgrey").pack(pady=20)

        # Create a frame for the table
        table_frame = tk.Frame(self, bg="lightgrey")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview widget) with custom style
        self.table = ttk.Treeview(
            table_frame,
            style="Custom.Treeview",
            columns=("name", "email", "request_date", "quantity", "price", "product"),
            show="headings"
        )

        # Define headings and column widths
        self.table.heading("name", text="Name")
        self.table.heading("email", text="Email")
        self.table.heading("request_date", text="Request Date")
        self.table.heading("quantity", text="Quantity")
        self.table.heading("price", text="Price")
        self.table.heading("product", text="Product")

        self.table.column("name", width=120)
        self.table.column("email", width=180)
        self.table.column("request_date", width=100)
        self.table.column("quantity", width=70, anchor="center")
        self.table.column("price", width=80, anchor="center")
        self.table.column("product", width=120)

        # Add sample data to the table
        self.populate_table()

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the table into the frame
        self.table.pack(fill="both", expand=True)

        # Create buttons for Approve and Decline actions
        button_frame = tk.Frame(self, bg="lightgrey")
        button_frame.pack(pady=10)

        self.approve_button = tk.Button(button_frame, text="Approve", command=lambda: self.prepare_signature("Approved"), bg="#4CAF50", fg="white")
        self.approve_button.pack(side="left", padx=10)

        self.decline_button = tk.Button(button_frame, text="Decline", command=lambda: self.prepare_signature("Declined"), bg="#F44336", fg="white")
        self.decline_button.pack(side="left", padx=10)

        self.signature_canvas_frame = None
        self.signature_canvas = None
        self.confirm_button = None

    def populate_table(self):
        """Populates the table with sample data."""
        sample_data = [
            ("Alice Johnson", "alice@example.com", "2024-01-01", 10, "$100", "Product A"),
            ("Bob Smith", "bob@example.com", "2024-01-05", 5, "$50", "Product B"),
            ("Carol White", "carol@example.com", "2024-01-10", 7, "$70", "Product C"),
            ("Dave Lee", "dave@example.com", "2024-01-12", 3, "$30", "Product D"),
            ("Eve Adams", "eve@example.com", "2024-01-15", 2, "$20", "Product E"),
        ]

        for row in sample_data:
            self.table.insert("", "end", values=row)

    def prepare_signature(self, status):
        """Displays the signature canvas and confirm button based on the action."""
        selected_item = self.table.selection()
        if not selected_item:
            return  # No item selected

        # Remove any existing signature canvas or buttons
        if self.signature_canvas_frame:
            self.signature_canvas_frame.destroy()

        # Create a frame for the signature canvas
        self.signature_canvas_frame = tk.Frame(self, bg="lightgrey")
        self.signature_canvas_frame.pack(pady=20)

        # Create canvas for signature
        self.signature_canvas = tk.Canvas(self.signature_canvas_frame, width=300, height=100, bg="white", bd=2)
        self.signature_canvas.pack()

        # Bind mouse events to allow drawing on the canvas
        self.signature_canvas.bind("<B1-Motion>", self.draw_signature)

        # Create a button to confirm the signature
        self.confirm_button = tk.Button(self.signature_canvas_frame, text="Confirm", command=lambda: self.submit_request(status))
        self.confirm_button.pack(pady=10)

    def draw_signature(self, event):
        """Handles the drawing of the signature on the canvas."""
        x, y = event.x, event.y
        self.signature_canvas.create_oval(x-2, y-2, x+2, y+2, fill="black", outline="black")

    def submit_request(self, status):
        """Handles the submission of the request after the signature is drawn."""
        selected_item = self.table.selection()
        if selected_item:
            item_data = self.table.item(selected_item)["values"]
            print(f"{status}: {item_data}")  # Print the request status and selected item data

            # You can add logic here to store the request status and signature as needed

        # Reset the UI after submission
        if self.signature_canvas_frame:
            self.signature_canvas_frame.destroy()

        self.signature_canvas = None
        self.confirm_button = None

# To test the RequestItemScreen independently, you can create a root window and add it to this script.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    app = RequestItemScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
