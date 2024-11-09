import tkinter as tk
from PIL import Image, ImageTk
import requests

class ViewInventoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="lightgrey")
        self.master = master
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="View Inventory", font=("Arial", 16), bg="lightgrey").pack(pady=20)
        
        gallery_frame = tk.Frame(self, bg="lightgrey")
        gallery_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Fetching data from API
        inventory_data = self.fetch_inventory_data()

        # Number of columns for displaying product cards
        columns = 10  # Adjust as per your desired grid size

        # Display each product in the gallery in a grid layout
        for index, product in enumerate(inventory_data):
            row = index // columns
            col = index % columns
            self.add_product_card(gallery_frame, product).grid(row=row, column=col, padx=10, pady=10, sticky="n")

    def fetch_inventory_data(self):
        url = 'http://127.0.0.1:8000/api/products/'
        headers = {'Authorization': 'Token 9cf71eb2aa85c9b8f7786d7b3df15a5e017521ef'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # Returns the list of products
        else:
            print("Error fetching data")
            return []

    def add_product_card(self, frame, product):
        card = tk.Frame(frame, bg="white", relief="solid", bd=2, width=200, height=250)
        
        # Title
        title = tk.Label(card, text=product.get("title", "No Title"), font=("Arial", 12), wraplength=180)
        title.pack(pady=10)

        # Price
        price = tk.Label(card, text=f"Price: P{product.get('price', 'N/A')}", font=("Arial", 10))
        price.pack(pady=5)

        # Stock
        stock = tk.Label(card, text=f"Stock: {product.get('stock', 'N/A')}", font=("Arial", 10))
        stock.pack(pady=5)

        # Category
        category = tk.Label(card, text=f"Category: {product.get('category', {}).get('name', 'No Category')}", font=("Arial", 10))
        category.pack(pady=5)

        # Image
        image_url = product.get('image')
        if image_url:
            try:
                # Download image using Pillow
                img_response = requests.get(image_url)
                img_response.raise_for_status()  # Raise exception for bad responses

                # Open image using Pillow
                image = Image.open(img_response.raw)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(card, image=photo)
                image_label.image = photo  # Keep a reference to the image
                image_label.pack(pady=5)
            except Exception as e:
                print(f"Error loading image: {e}")
                image_label = tk.Label(card, text="Image Unavailable", font=("Arial", 8))
                image_label.pack(pady=5)
        else:
            image_label = tk.Label(card, text="No Image", font=("Arial", 8))
            image_label.pack(pady=5)

        return card
