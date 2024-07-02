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
    filename_var = None
    hidefilename_var = None
    onetime_var = None
    password_var = None
    expire_var = None

    def upload_file(self):
        file_path = filedialog.askopenfilename()

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.filename_var.delete(0, tk.END)
            self.filename_var.insert(tk.END, file_path)

    def render(self, output_frame):
        self.root = output_frame
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="WaifuVault Uploader", font=header_font)
        header_label.pack(anchor="nw")

        button_upper_frame = tk.Frame(output_frame)
        button_upper_frame.pack(fill=tk.X)
        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X)
        button_lower_frame = tk.Frame(output_frame)
        button_lower_frame.pack(fill=tk.X)

        filename_label = tk.Label(button_upper_frame, text="File:")
        filename_label.pack(side="left", padx=5)
        self.filename_var = tk.Entry(button_upper_frame, width=65)
        self.filename_var.pack(side="left", padx=5)
        choosefile_button = tk.Button(button_upper_frame, text="Browse", command=self.choose_file)
        choosefile_button.pack(side="left", padx=5)

        self.hidefilename_var = tk.BooleanVar(value=False)
        hidefilename_flag = tk.Checkbutton(button_frame, text="Hide Filename", variable=self.hidefilename_var)
        hidefilename_flag.pack(side="left", padx=5)

        self.onetime_var = tk.BooleanVar(value=False)
        onetime_flag = tk.Checkbutton(button_frame, text="One Time Download", variable=self.onetime_var)
        onetime_flag.pack(side="left", padx=5)

        expire_label = tk.Label(button_frame, text="Expire:")
        expire_label.pack(side="left")
        self.expire_var = tk.StringVar(value="Compute")
        expire_menu = tk.OptionMenu(button_frame, self.expire_var, "Compute", "1 Hour", "1 Day", "1 Week", "1 Month", "1 Year")
        expire_menu.config(width=6)
        expire_menu.pack(side="left", padx=5)

        password_label = tk.Label(button_frame, text="Password:")
        password_label.pack(side="left", padx=5)
        self.password_var = tk.Entry(button_frame, width=22)
        self.password_var.pack(side="left", padx=5)

        upload_button = tk.Button(button_lower_frame, text="Upload", command=self.upload_file)
        upload_button.pack(side="left", padx=5)
