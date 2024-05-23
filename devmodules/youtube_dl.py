# Youtube Downloader module
import tkinter as tk
from tkinter import font, filedialog, messagebox
import yt_dlp
from devmodules import basedevtools as base


class youtube_dl(base.basedevtools):
    display_name = "YouTube Downloader"
    category = "Image tools"
    output_text_frame = None
    output_context_menu = None
    url_entry = None
    resolution_var = None
    root = None

    def download(self):
        downloaded_files = []

        def hook(d):
            if d['status'] == 'finished':
                downloaded_files.append(d['filename'])

        url = self.url_entry.get()
        if url:
            try:
                self.output_text_frame.config(state=tk.NORMAL)
                self.output_text_frame.insert(tk.END,f"Downloading {url}...\n")

                filepath = filedialog.askdirectory()

                ydl_opts = {
                    'format': 'best[ext=mp4]/best',
                    'paths': {'home': filepath},
                    'progress_hooks': [hook],
                }

                resolution = self.resolution_var.get()
                match resolution:
                    case "Highest":
                        ydl_opts['format'] = 'best[ext=mp4]/best'
                    case "Lowest":
                        ydl_opts['format'] = 'worst[ext=mp4]/worst'
                    case "Audio":
                        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio'
                    case _:
                        ydl_opts['format'] = 'best[ext=mp4]/best'

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    error_code = ydl.download([url])
                savedpath = downloaded_files[0]
                self.output_text_frame.insert(tk.END,f"Saved to {savedpath}\n")
                self.output_text_frame.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download: {e}")

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
        header_label = tk.Label(output_frame, text="YouTube Downloader", font=header_font)
        header_label.pack(anchor="nw")

        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.url_entry = tk.Entry(button_frame, width=50)
        self.url_entry.pack(side="left", padx=5)

        resolution_label = tk.Label(button_frame, text="Resolution:")
        resolution_label.pack(side="left")
        self.resolution_var = tk.StringVar(value="Highest")
        resolution_menu = tk.OptionMenu(button_frame, self.resolution_var, "Highest", "Lowest", "Audio")
        resolution_menu.config(width=6)
        resolution_menu.pack(side="left", padx=5)

        download_button = tk.Button(button_frame, text="Download", command=self.download)
        download_button.pack(side="left", padx=5)

        self.output_text_frame = tk.Text(output_frame, state=tk.DISABLED, width=80)
        self.output_text_frame.bind("<Button-2>", self.show_output_context_menu)
        self.output_text_frame.bind("<Button-3>", self.show_output_context_menu)
        self.output_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

        self.output_context_menu = tk.Menu(self.output_text_frame, tearoff=0)
        self.output_context_menu.add_command(label="Copy", command=self.copy_output)