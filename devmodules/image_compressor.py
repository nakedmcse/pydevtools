# Image Compressor
import tkinter as tk
from tkinter import font, filedialog, messagebox
from PIL import Image, ImageTk

from devmodules import basedevtools as base


class image_compressor(base.basedevtools):
    display_name = "Image Compressor"
    category = "Image tools"
    image_label = None
    photo = None
    image = None
    output_context_menu = None
    root = None

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = Image.open(file_path)
                self.photo = ImageTk.PhotoImage(self.image)
                self.image_label.config(image=self.photo)
                self.image_label.image = self.photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def compress_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            try:
                self.image.save(file_path, optimize=True, quality=85)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def render(self, output_frame):
        self.root = output_frame
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="Image Compressor", font=header_font)
        header_label.pack(anchor="nw")

        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X, pady=5)

        load_button = tk.Button(button_frame, text="Load", command=self.load_file)
        load_button.pack(side="left", padx=5)

        compress_button = tk.Button(button_frame, text="Compress", command=self.compress_file)
        compress_button.pack(side="left", padx=5)

        self.image_label = tk.Label(output_frame)
        self.image_label.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
