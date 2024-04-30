# JSON pretty print module
import tkinter as tk
from tkinter import ttk, font

from devmodules import basedevtools as base


class json_prettyprint(base.basedevtools):
    display_name = "JSON Pretty Printer"
    category = "Format tools"
    input_text = ""
    output_text = ""

    def render(self, output_frame):
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="JSON Pretty Printer", font=header_font)
        header_label.pack(anchor="nw")

        input_text_frame = tk.Text(output_frame, width=40)
        output_text_frame = tk.Text(output_frame, state=tk.DISABLED, width=40)
        input_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
        output_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
