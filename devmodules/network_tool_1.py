# Test module
import tkinter as tk
from tkinter import ttk, font
from devmodules import basedevtools as base


class test_module_1(base.basedevtools):
    display_name = "Some Network Tool"
    category = "Network tools"

    def render(self, output_frame):
        output_text = tk.Text(output_frame, state=tk.DISABLED)
        output_text.pack(expand=True, fill=tk.BOTH)
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Some Network Tool\n")
        output_text.config(state=tk.DISABLED)

