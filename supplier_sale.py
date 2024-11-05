import tkinter as tk

class SupplierSaleScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Supplier Sale Screen", font=("Arial", 16)).pack(expand=True)
