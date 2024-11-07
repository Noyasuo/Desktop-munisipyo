import tkinter as tk

class ViewInventoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="View Inventory", font=("Arial", 16), bg="lightgrey").pack(pady=20)
        
        gallery_frame = tk.Frame(self, bg="lightgrey")
        gallery_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Sample static inventory data
        inventory_data = [
            {"name": "Product A", "available": True, "quantity": 10},
            {"name": "Product B", "available": False, "quantity": 0},
            {"name": "Product C", "available": True, "quantity": 7},
            {"name": "Product D", "available": True, "quantity": 3},
            {"name": "Product E", "available": False, "quantity": 0},
            {"name": "Product F", "available": True, "quantity": 5},
            {"name": "Product G", "available": True, "quantity": 2},
            {"name": "Product H", "available": False, "quantity": 1},
            {"name": "Product I", "available": True, "quantity": 8},
            {"name": "Product J", "available": True, "quantity": 6},
            {"name": "Product K", "available": True, "quantity": 4},
            # Add more products as needed
        ]

        # Number of columns for displaying product cards
        columns = 10

        # Display each product in the gallery in a grid layout
        for index, product in enumerate(inventory_data):
            row = index // columns
            col = index % columns
            self.add_product_card(gallery_frame, product).grid(row=row, column=col, padx=10, pady=10, sticky="n")

    def add_product_card(self, parent, product):
        # Create a frame for each product card
        card_frame = tk.Frame(parent, bg="white", padx=10, pady=10, relief="raised", borderwidth=1)

        # Placeholder for the image box
        img_label = tk.Label(card_frame, text="No Image", bg="grey", fg="white", width=15, height=5)
        img_label.pack()

        # Display product name
        name_label = tk.Label(card_frame, text=product["name"], font=("Arial", 12, "bold"), bg="white")
        name_label.pack(pady=5)

        # Display availability and quantity
        status_text = "Available" if product["available"] else "Unavailable"
        status_color = "green" if product["available"] else "red"
        status_label = tk.Label(card_frame, text=f"Status: {status_text}", fg=status_color, bg="white")
        status_label.pack()

        quantity_label = tk.Label(card_frame, text=f"Quantity: {product['quantity']}", bg="white")
        quantity_label.pack()

        return card_frame
