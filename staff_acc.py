import tkinter as tk

class StaffAccScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Staff Accounts Screen", font=("Arial", 16)).pack(expand=True)
