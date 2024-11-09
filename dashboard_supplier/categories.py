import tkinter as tk

class CategoriesScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#f5f5f5")
        label = tk.Label(self, text="Categories", font=("Arial", 18), bg="#f5f5f5")
        label.pack(pady=20)
