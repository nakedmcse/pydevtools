# Test module
import tkinter as tk
from tkinter import ttk, font

from devmodules import basedevtools as base


class test_module_3(base.basedevtools):
    display_name = "Some Encoding Tool"
    category = "Encoding tools"

    def render(self, output_frame):
        output_text = tk.Text(output_frame, state=tk.DISABLED)
        output_text.pack(expand=True, fill=tk.BOTH)
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Some Encoding Tool\n")
        output_text.config(state=tk.DISABLED)
