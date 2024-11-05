import tkinter as tk

class RequestItemScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Request Item Screen", font=("Arial", 16)).pack(expand=True)
