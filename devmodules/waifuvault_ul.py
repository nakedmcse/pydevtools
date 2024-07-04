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
        file_path = self.filename_var.get()
        password = self.password_var.get()
        if password == '':
            password = None
        match self.expire_var.get():
            case "Compute":
                expires = None
            case "1 Hour":
                expires = "1h"
            case "1 Day":
                expires = "1d"
            case "1 Week":
                expires = "1w"
            case "1 Month":
                expires = "30d"
            case "1 Year":
                expires = "365d"

        if file_path:
            upload = waifuvault.FileUpload(target=file_path, oneTimeDownload=self.onetime_var.get(),
                                           hidefilename=self.hidefilename_var.get(), password=password, expires=expires)
            try:
                upload_res = waifuvault.upload_file(upload)
                self.output_text_frame.config(state=tk.NORMAL)
                self.output_text_frame.insert(tk.END, f"Token: {upload_res.token}\nURL: {upload_res.url}\nRetention: {upload_res.retentionPeriod}\nEncrypted: {upload_res.options.protected}\nOne Time Download: {upload_res.options.oneTimeDownload}\n\n")
                self.output_text_frame.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed: {e}")


    def choose_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.filename_var.delete(0, tk.END)
            self.filename_var.insert(tk.END, file_path)

    def show_output_context_menu(self,event):
        self.output_context_menu.post(event.x_root, event.y_root)

    def show_input_context_menu(self,event):
        self.input_context_menu.post(event.x_root, event.y_root)

    def copy_output(self, event=None):
        try:
            text_content = self.output_text_frame.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(text_content)
        except tk.TclError:
            # handle nothing selected
            pass

    def paste_input(self, event=None):
        try:
            start = self.filename_var.index("sel.first")
            end = self.filename_var.index("sel.last")
            self.filename_var.delete(start, end)
        except tk.TclError:
            # handle nothing selected
            pass
        try:
            text_content = self.root.clipboard_get()
            self.filename_var.insert(tk.INSERT, text_content)
        except tk.TclError:
            # handle nothing in clipboard
            pass

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
        self.filename_var.bind("<Button-2>", self.show_input_context_menu)
        self.filename_var.bind("<Button-3>", self.show_input_context_menu)
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

        self.output_text_frame = tk.Text(output_frame, state=tk.DISABLED, width=60)
        self.output_text_frame.bind("<Button-2>", self.show_output_context_menu)
        self.output_text_frame.bind("<Button-3>", self.show_output_context_menu)
        self.output_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.output_context_menu = tk.Menu(self.output_text_frame, tearoff=0)
        self.output_context_menu.add_command(label="Copy", command=self.copy_output)

        self.input_context_menu = tk.Menu(self.filename_var, tearoff=0)
        self.input_context_menu.add_command(label="Paste", command=self.paste_input)