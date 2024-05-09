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
    resized_image = None
    output_context_menu = None
    root = None

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = Image.open(file_path)

                # Get the dimensions of the label
                label_width = self.image_label.winfo_width()
                label_height = self.image_label.winfo_height()

                # Calculate the ratio to maintain aspect ratio
                img_width, img_height = self.image.size
                ratio_width = label_width / img_width
                ratio_height = label_height / img_height
                scale_ratio = min(ratio_width, ratio_height)

                # Calculate new dimensions
                new_width = int(img_width * scale_ratio)
                new_height = int(img_height * scale_ratio)

                # Resize image
                self.resized_image = self.image.resize((new_width, new_height))

                self.photo = ImageTk.PhotoImage(self.resized_image)
                self.image_label.config(image=self.photo)
                self.image_label.image = self.photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def compress_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            try:
                self.image.save(file_path, optimize=True, quality=60)
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

        self.image_label = tk.Label(output_frame, width=80)
        self.image_label.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
