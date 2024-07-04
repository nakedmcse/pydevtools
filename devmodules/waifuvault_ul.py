# Waifuvault uploader module
import tkinter as tk
from tkinter import font, filedialog, messagebox
import waifuvault
from devmodules import basedevtools as base


class waifuvault_ul(base.basedevtools):
    display_name = "WaifuVault Uploader"
    category = "File tools"
    output_text_frame = None
    results_frame = None
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

                new_entry_frame = tk.Frame(self.results_frame, pady=5)
                new_entry_frame.pack(fill=tk.X)
                entry_upper_line = tk.Frame(new_entry_frame)
                entry_upper_line.pack(fill=tk.X)
                entry_lower_line = tk.Frame(new_entry_frame)
                entry_lower_line.pack(fill=tk.X)

                url_entry = tk.Entry(entry_upper_line, width=70)
                url_entry.insert(tk.END, upload_res.url)
                url_entry.pack(side="left", padx=5)

                copy_url_button = tk.Button(entry_upper_line, text="Copy URL", command=lambda: self.copy_clip(upload_res.url))
                copy_url_button.pack(side="left", padx=5)

                token_entry = tk.Entry(entry_lower_line, width=35)
                token_entry.insert(tk.END, upload_res.token)
                token_entry.pack(side="left", padx=5)

                copy_token_button = tk.Button(entry_lower_line, text="Copy Token", command=lambda: self.copy_clip(upload_res.token))
                copy_token_button.pack(side="left", padx=5)
                edit_entry_button = tk.Button(entry_lower_line, text="Edit", command=lambda: self.edit_entry(upload_res.token))
                edit_entry_button.pack(side="left", padx=5)
                delete_entry_button = tk.Button(entry_lower_line, text="Delete", command=lambda: self.delete_entry(upload_res.token, new_entry_frame))
                delete_entry_button.pack(side="left", padx=5)
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed: {e}")

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.filename_var.delete(0, tk.END)
            self.filename_var.insert(tk.END, file_path)

    def copy_clip(self, target: str):
        self.root.clipboard_clear()
        self.root.clipboard_append(target)

    def edit_entry(self, token: str):
        try:
            entry_info = waifuvault.file_info(token, True)

            edit_window = tk.Tk()
            edit_window.title("Edit Entry")
            edit_window.geometry("640x480")

            output_text_frame = tk.Text(edit_window, state=tk.DISABLED, width=40)
            output_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
            output_text_frame.config(state=tk.NORMAL)
            output_text_frame.delete(1.0, tk.END)
            output_text_frame.insert(tk.END, f"URL: {entry_info.url}\nRetention: {entry_info.retentionPeriod}\n")
            output_text_frame.config(state=tk.DISABLED)

            edit_exit = tk.Button(edit_window, text="Exit", command=edit_window.destroy)
            edit_exit.pack(side="top", pady=15)
        except Exception as e:
            messagebox.showerror("Error", f"Edit failed: {e}")

    def delete_entry(self, token: str, target: any):
        try:
            waifuvault.delete_file(token)
            target.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")

    def show_input_context_menu(self, event):
        self.input_context_menu.post(event.x_root, event.y_root)

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

        self.results_frame = tk.Frame(output_frame, pady=15)
        self.results_frame.pack(fill=tk.X)