# Waifuvault uploader module
import tkinter as tk
from tkinter import font, filedialog, messagebox
import waifuvault
from devmodules import basedevtools as base


class waifuvault_ul(base.basedevtools):
    display_name = "WaifuVault Uploader"
    category = "File tools"
    output_text_frame = None
    output_context_menu = None
    input_context_menu = None
    root = None
    hidefilename_var = None
    onetime_var = None

    def render(self, output_frame):
        self.root = output_frame
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="WaifuVault Uploader", font=header_font)
        header_label.pack(anchor="nw")

        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.hidefilename_var = tk.BooleanVar(value=False)
        hidefilename_flag = tk.Checkbutton(button_frame, text="Hide Filename", variable=self.hidefilename_var)
        hidefilename_flag.pack(side="left", padx=5)

        self.onetime_var = tk.BooleanVar(value=False)
        onetime_flag = tk.Checkbutton(button_frame, text="One Time Download", variable=self.onetime_var)
        onetime_flag.pack(side="left", padx=5)

        upload_button = tk.Button(button_frame, text="Upload", command=self.upload_file)
        upload_button.pack(side="left", padx=5)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_file)
        delete_button.pack(side="left", padx=5)

        self.comp_level = tk.Label(button_frame)
        self.comp_level.pack(side="left", padx=10)

        self.image_label = tk.Label(output_frame, width=80)
        self.image_label.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
