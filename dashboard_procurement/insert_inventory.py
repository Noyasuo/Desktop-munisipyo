import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class InsertInventoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.configure(bg="lightgrey")

        # Create the card frame with padding to move it down a bit
        card_frame = tk.Frame(self, bg="white", padx=20, pady=20, relief="raised", borderwidth=2)
        card_frame.pack(padx=20, pady=(40, 20))  # Add more space at the top to move the card down

        # Title for the Insert Inventory screen inside the card
        tk.Label(card_frame, text="Insert Inventory Screen", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

        # Product Title
        tk.Label(card_frame, text="Product Title", bg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.product_title_entry = tk.Entry(card_frame, font=("Arial", 12), width=30)
        self.product_title_entry.grid(row=1, column=1, padx=10, pady=5)

        # Categories (Dropdown) with fixed default text
        tk.Label(card_frame, text="Categories", bg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.categories_combobox = ttk.Combobox(card_frame, font=("Arial", 12), width=28, values=["Office Supply", "Cleaning Supply", "Electronics Supply"])
        self.categories_combobox.set("Select Categories")  # Default value
        self.categories_combobox['state'] = 'readonly'  # Make the default text fixed and non-editable
        self.categories_combobox.grid(row=2, column=1, padx=10, pady=5)

        # Product Image (File Selector)
        tk.Label(card_frame, text="Product Image", bg="white", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.image_path_label = tk.Label(card_frame, text="No file chosen", bg="white", font=("Arial", 10))
        self.image_path_label.grid(row=3, column=1, sticky="w", padx=(100, 10), pady=5)
        self.image_button = tk.Button(card_frame, text="Choose File", command=self.select_image, font=("Arial", 10))
        self.image_button.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Product Price
        tk.Label(card_frame, text="Product Price", bg="white", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.product_price_entry = tk.Entry(card_frame, font=("Arial", 12), width=30)
        self.product_price_entry.grid(row=4, column=1, padx=10, pady=5)

        # Quantity
        tk.Label(card_frame, text="Quantity", bg="white", font=("Arial", 12)).grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.quantity_entry = tk.Entry(card_frame, font=("Arial", 12), width=10)
        self.quantity_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Insert Product Button (Initially disabled)
        self.insert_product_button = tk.Button(card_frame, text="Insert Product", font=("Arial", 12), command=self.insert_product, state="disabled")
        self.insert_product_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Bind events to update button state whenever any field is modified
        self.product_title_entry.bind("<KeyRelease>", self.check_fields)
        self.categories_combobox.bind("<<ComboboxSelected>>", self.check_fields)
        self.product_price_entry.bind("<KeyRelease>", self.check_fields)
        self.quantity_entry.bind("<KeyRelease>", self.check_fields)

    def select_image(self):
        """Open file dialog to select an image file and update the label."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.image_path_label.config(text=file_path)
            self.check_fields()  # Check fields to update button state

    def check_fields(self, event=None):
        """Enable the Insert Product button only if all fields are filled."""
        if (self.product_title_entry.get().strip() and
            self.categories_combobox.get() != "Select Categories" and
            self.image_path_label.cget("text") != "No file chosen" and
            self.product_price_entry.get().strip() and
            self.quantity_entry.get().strip()):
            self.insert_product_button.config(state="normal")  # Enable button
        else:
            self.insert_product_button.config(state="disabled")  # Disable button

    def insert_product(self):
        """Function to handle the insertion of the product."""
        product_title = self.product_title_entry.get()
        category = self.categories_combobox.get()
        image_path = self.image_path_label.cget("text")
        product_price = self.product_price_entry.get()
        quantity = self.quantity_entry.get()

        # Handle form submission (e.g., save to database)
        print("Product Title:", product_title)
        print("Category:", category)
        print("Image Path:", image_path)
        print("Product Price:", product_price)
        print("Quantity:", quantity)
        
        # Display a success message
        messagebox.showinfo("Insert Product", "Product inserted successfully!")
