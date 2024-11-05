import tkinter as tk

class SupplierAccScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Supplier Accounts Screen", font=("Arial", 16)).pack(expand=True)
