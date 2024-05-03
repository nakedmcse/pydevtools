# JPG EXIF viewer module
import os
import tkinter as tk
from tkinter import font, filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS
from devmodules import basedevtools as base


class jpg_exif(base.basedevtools):
    display_name = "JPG EXIF Viewer"
    category = "Image tools"
    output_text_frame = None
    output_context_menu = None
    root = None

    def load_file(self):
        file_path = filedialog.askopenfilename(defaultextension="jpg")
        if file_path:
            try:
                self.output_text_frame.config(state=tk.NORMAL)
                image = Image.open(file_path)
                # basic image info
                info_dict = {
                    "Filename": os.path.basename(file_path),
                    "Image Size": image.size,
                    "Image Height": image.height,
                    "Image Width": image.width,
                    "Image Format": image.format,
                    "Image Mode": image.mode,
                    "Image is Animated": getattr(image, "is_animated", False),
                    "Frames in Image": getattr(image, "n_frames", 1)
                }

                self.output_text_frame.delete(1.0, tk.END)

                for label, value in info_dict.items():
                    self.output_text_frame.insert(tk.END, f"{label:25}: {value}\n")

                # exif info
                exif_data = image.getexif()

                for tag_id in exif_data:
                    # get tag name
                    tag = TAGS.get(tag_id, tag_id)
                    data = exif_data.get(tag_id)
                    # decode bytes
                    if isinstance(data, bytes):
                        data = data.decode()
                    self.output_text_frame.insert(tk.END, f"{tag:25}: {data}\n")

                self.output_text_frame.config(state=tk.DISABLED)
                image.close()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def copy_output(self, event=None):
        try:
            text_content = self.output_text_frame.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(text_content)
        except tk.TclError:
            # handle nothing selected
            pass

    def show_output_context_menu(self, event):
        self.output_context_menu.post(event.x_root, event.y_root)

    def render(self, output_frame):
        self.root = output_frame
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="JPG EXIF Viewer", font=header_font)
        header_label.pack(anchor="nw")

        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X, pady=5)

        load_button = tk.Button(button_frame, text="Load", command=self.load_file)
        load_button.pack(side="left", padx=5)

        self.output_text_frame = tk.Text(output_frame, state=tk.DISABLED, width=40)
        self.output_text_frame.bind("<Button-2>", self.show_output_context_menu)
        self.output_text_frame.bind("<Button-3>", self.show_output_context_menu)
        self.output_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

        self.output_context_menu = tk.Menu(self.output_text_frame, tearoff=0)
        self.output_context_menu.add_command(label="Copy", command=self.copy_output)