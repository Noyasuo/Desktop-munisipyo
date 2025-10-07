import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
from login import TOKEN

class ApprovedScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_style()
        self.create_widgets()

    def create_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background="lightgrey",
                        foreground="black",
                        rowheight=30,
                        font=("Arial", 10))
        style.map("Custom.Treeview",
                  background=[("selected", "#397D49")],
                  foreground=[("selected", "white")])

    def create_widgets(self):
        tk.Label(self, text="Approved Requests", font=("Arial", 16, "bold")).pack(pady=20)

        table_frame = tk.Frame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("Order Id", "Name", "Email", "Request Date", "Quantity", "Item", "Barcode"), show="headings", style="Custom.Treeview")

        headings = ["Order Id", "Name", "Email", "Request Date", "Quantity", "Item", "Barcode"]
        column_widths = [120, 150, 120, 100, 150, 150]

        for col, width in zip(headings, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.populate_table()

        self.tree.bind("<ButtonRelease-1>", self.on_row_selected)

        self.action_frame = tk.Frame(self, bg="lightgrey")
        self.action_frame.pack(pady=10)
        self.dispatch_button = tk.Button(self.action_frame, text="Dispatch", command=self.dispatch_request, state="disabled", bg="blue", fg="white")
        self.dispatch_button.grid(row=0, column=0, padx=10)

    def populate_table(self):
        from config import API_BASE_URL
        url = f"{API_BASE_URL}/api/orders/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}'
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                for order in data:
                    if order['final_status'] == 'approved':
                        user_name = order['user']['username']
                        user_email = order['user']['email']
                        request_date = order['request_date']
                        quantity = order['quantity']
                        order_id = order['id']
                        item_names = ', '.join([product['title'] for product in order['product']])
                        barcodes = ', '.join([product['barcode'] for product in order['product']])
                        self.tree.insert("", "end", values=(order_id, user_name, user_email, request_date, quantity, item_names, barcodes))
            else:
                messagebox.showerror("Error", "Failed to retrieve orders data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_row_selected(self, event):
        if self.tree.selection():
            self.selected_row_id = self.tree.selection()[0]
            self.dispatch_button.config(state="normal")

    def dispatch_request(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)['values']
            order_id, user_name, user_email, request_date, quantity, item_names, barcodes = item_values

            dispatch_frame = tk.Frame(self, bg="lightgrey")
            dispatch_frame.pack(pady=20)

            fields = ["Name", "Email", "Request Date", "Quantity", "Item", "Barcode"]
            values = [user_name, user_email, request_date, quantity, item_names, barcodes]
            entries = {}

            for i, (field, value) in enumerate(zip(fields, values)):
                tk.Label(dispatch_frame, text=field, bg="lightgrey").grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(dispatch_frame)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, value)
                entries[field] = entry

            confirm_button = tk.Button(dispatch_frame, text="Confirm", command=lambda: self.show_signature_ui(dispatch_frame, selected_item, entries, order_id))
            confirm_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

    def add_barcode(self, barcode_entry, confirm_button):
        barcode = barcode_entry.get().strip()
        if barcode and barcode not in self.scanned_barcodes:
            self.scanned_barcodes.add(barcode)
            barcode_entry.insert(tk.END, f" {barcode}")
            confirm_button.config(state="normal")

    def show_signature_ui(self, dispatch_frame, selected_item, entries, order_id):
        signature_window = tk.Toplevel(self.master)
        signature_window.title("Signature")
        signature_window.geometry("400x300")
        signature_window.transient(self.master)
        signature_window.grab_set()
        signature_window.update_idletasks()
        x = (signature_window.winfo_screenwidth() - signature_window.winfo_reqwidth()) // 2
        y = (signature_window.winfo_screenheight() - signature_window.winfo_reqheight()) // 2
        signature_window.geometry(f"+{x}+{y}")

        tk.Label(signature_window, text="Please sign below:", font=("Arial", 14)).pack(pady=10)

        signature_canvas = tk.Canvas(signature_window, bg="white", width=350, height=200)
        signature_canvas.pack(pady=10)

        def clear_canvas():
            signature_canvas.delete("all")

        def save_signature():
            self.confirm_dispatch(dispatch_frame, selected_item, entries, order_id)
            signature_window.destroy()

        signature_canvas.bind("<B1-Motion>", lambda event: self.draw_signature(event, signature_canvas))

        tk.Button(signature_window, text="Clear", command=clear_canvas).pack(side="left", padx=10)
        tk.Button(signature_window, text="Confirm", command=save_signature).pack(side="right", padx=10)

    def draw_signature(self, event, canvas):
        x, y = event.x, event.y
        canvas.create_oval(x, y, x+2, y+2, fill="black")

    def clear_canvas(self):
        self.signature_canvas.delete("all")

    def confirm_dispatch(self, frame, selected_item, entries, order_id):
        print(f"Dispatching request for item: {entries} {order_id}")

        url = f"http://localhost:8000/api/order/{order_id}/"
        headers = {
            'accept': 'application/json',
            'Authorization': f'Token {TOKEN}',
            'Content-Type': 'application/json'
        }
        data = {
            "final_status": "dispatch",
            "status": "dispatch"
        }

        try:
            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Dispatch", "The selected request has been dispatched successfully.")
            else:
                messagebox.showerror("Error", "Failed to update the order status.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.tree.delete(selected_item)
        frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = ApprovedScreen(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()