# JSON pretty print module
import tkinter as tk
from tkinter import ttk, font

from devmodules import basedevtools as base


class json_prettyprint(base.basedevtools):
    display_name = "JSON Pretty Printer"
    category = "Format tools"
    input_text = ""
    output_text = ""

    def render(self, pane, output_frame):
        output_frame.destroy()
        output_frame = ttk.Frame(pane, width=500)

        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="JSON Pretty Printer", font=header_font)
        header_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)

        input_text_frame = tk.Text(output_frame)
        input_text_frame.grid(row=1, column=0, sticky="w", padx=5)

        output_text_frame = tk.Text(output_frame, state=tk.DISABLED)
        output_text_frame.grid(row=1, column=1, sticky="w", padx=5)

        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_columnconfigure(1, weight=1)
