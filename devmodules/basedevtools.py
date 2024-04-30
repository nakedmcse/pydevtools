# Base module class
import tkinter as tk


class basedevtools:
    def __init__(self, display_name: str, category: str):
        self.display_name = display_name
        self.category = category

    def render(self, output_frame):
        output_text = tk.Text(output_frame, state=tk.DISABLED)
        output_text.pack(expand=True, fill=tk.BOTH)
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, self.display_name)
        output_text.config(state=tk.DISABLED)