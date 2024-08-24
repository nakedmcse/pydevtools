# Waifuvault uploader module
import tkinter as tk
from tkinter import font, filedialog, messagebox
import waifuvault
from devmodules import basedevtools as base
import time


class waifuvault_ul(base.basedevtools):
    display_name = "WaifuVault Uploader"
    category = "File tools"
    output_text_frame = None
    results_frame = None
    output_context_menu = None
    input_context_menu = None
    bucket_context_menu = None
    root = None
    button_upper_frame = None
    bucket_frame = None
    filename_var = None
    hidefilename_var = None
    onetime_var = None
    password_var = None
    expire_var = None
    old_password_var = None
    new_password_var = None
    opts_hidefilename_var = None
    opts_expire_var = None
    upload_button = None
    validate_import_var = None
    bucket_token_var = None

    def insert_entry(self, upload_res: waifuvault.FileResponse):
        new_entry_frame = tk.Frame(self.results_frame, pady=5)
        new_entry_frame.pack(fill=tk.X)
        entry_upper_line = tk.Frame(new_entry_frame)
        entry_upper_line.pack(fill=tk.X)
        entry_lower_line = tk.Frame(new_entry_frame)
        entry_lower_line.pack(fill=tk.X)

        url_entry = tk.Entry(entry_upper_line, name="url", width=70)
        url_entry.insert(tk.END, upload_res.url)
        url_entry.pack(side="left", padx=5)

        copy_url_button = tk.Button(entry_upper_line, text="Copy URL", command=lambda: self.copy_clip(upload_res.url))
        copy_url_button.pack(side="left", padx=5)

        token_entry = tk.Entry(entry_lower_line, name="token", width=35)
        token_entry.insert(tk.END, upload_res.token)
        token_entry.pack(side="left", padx=5)

        copy_token_button = tk.Button(entry_lower_line, text="Copy Token", command=lambda: self.copy_clip(upload_res.token))
        copy_token_button.pack(side="left", padx=5)
        edit_entry_button = tk.Button(entry_lower_line, text="Edit", command=lambda: self.edit_entry(upload_res.token, url_entry))
        edit_entry_button.pack(side="left", padx=5)
        delete_entry_button = tk.Button(entry_lower_line, text="Delete", command=lambda: self.delete_entry(upload_res.token, new_entry_frame))
        delete_entry_button.pack(side="left", padx=5)

    def upload_file(self):
        file_path = self.filename_var.get()
        bucket = self.bucket_token_var.get()
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
            upload = waifuvault.FileUpload(target=file_path, bucket_token=bucket, oneTimeDownload=self.onetime_var.get(),
                                           hidefilename=self.hidefilename_var.get(), password=password, expires=expires)
            try:
                self.upload_button.config(state=tk.DISABLED)
                upload_res = waifuvault.upload_file(upload)
                self.upload_button.config(state=tk.NORMAL)
                self.insert_entry(upload_res)
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

    def edit_entry(self, token: str, url_entry: any):
        try:
            entry_info = waifuvault.file_info(token, True)

            edit_window = tk.Tk()
            edit_window.title("Edit Entry")
            edit_window.geometry("640x250")

            output_text_frame = tk.Text(edit_window, state=tk.DISABLED, width=40, height=5)
            output_text_frame.pack(side="top", fill=tk.X, expand=True, padx=5)
            output_text_frame.config(state=tk.NORMAL)
            output_text_frame.delete(1.0, tk.END)
            output_text_frame.insert(tk.END, f"URL: {entry_info.url}\nRetention: {entry_info.retentionPeriod}\nProtected: {entry_info.options.protected}\nOne Time Download: {entry_info.options.oneTimeDownload}\nHide Filename: {entry_info.options.hideFilename}\n")
            output_text_frame.config(state=tk.DISABLED)

            passwords_frame = tk.Frame(edit_window)
            passwords_frame.pack(side="top", pady=5)
            old_password_label = tk.Label(passwords_frame, text="Old Password:")
            old_password_label.pack(side="left", padx=5)
            self.old_password_var = tk.Entry(passwords_frame, width=15)
            self.old_password_var.pack(side="left", padx=5)
            new_password_label = tk.Label(passwords_frame, text="New Password:")
            new_password_label.pack(side="left", padx=5)
            self.new_password_var = tk.Entry(passwords_frame, width=15)
            self.new_password_var.pack(side="left", padx=5)

            options_frame = tk.Frame(edit_window)
            options_frame.pack(side="top", pady=5)
            self.opts_hidefilename_var = tk.BooleanVar(master=edit_window, value=entry_info.options.hideFilename)
            opts_hidefilename_flag = tk.Checkbutton(options_frame, text="Hide Filename", variable=self.opts_hidefilename_var)
            opts_hidefilename_flag.pack(side="left", padx=5)

            opts_expire_label = tk.Label(options_frame, text="Expire:")
            opts_expire_label.pack(side="left")
            self.opts_expire_var = tk.StringVar(master=edit_window, value="No Change")
            opts_expire_menu = tk.OptionMenu(options_frame, self.opts_expire_var, "No Change", "1 Hour", "1 Day", "1 Week", "1 Month", "1 Year")
            opts_expire_menu.config(width=10)
            opts_expire_menu.pack(side="left", padx=5)

            buttons = tk.Frame(edit_window)
            buttons.pack(side="top", pady=15)
            edit_update = tk.Button(buttons, text="Update Entry", command=lambda: self.update_entry(entry_info.token, edit_window, self.new_password_var.get(), self.old_password_var.get(), self.opts_hidefilename_var.get(), self.opts_expire_var.get(), url_entry))
            edit_update.pack(side="left", padx=5)
            edit_exit = tk.Button(buttons, text="Exit", command=edit_window.destroy)
            edit_exit.pack(side="left", padx=5)
            edit_window.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Edit failed: {e}")

    def update_entry(self, token: str, target: any, password: str, previous_password: str, hide_filename: bool, expire_var: str, url_entry: any):
        try:
            expires = None
            match expire_var:
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
            result = waifuvault.file_update(token, password, previous_password, expires, hide_filename)
            url_entry.delete(0, tk.END)
            url_entry.insert(tk.END, result.url)
            target.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    def delete_entry(self, token: str, target: any):
        try:
            waifuvault.delete_file(token)
            target.destroy()
        except Exception as e:
            response = messagebox.askyesno("Error", f"Delete failed: {e}\nRemove Entry ?")
            if response:
                target.destroy()

    def export_results(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            try:
                outtext = "token,url\n"
                for widget in self.results_frame.winfo_children():
                    token = ""
                    url = ""
                    for inner_widget in widget.winfo_children():
                        for leaf_widget in inner_widget.winfo_children():
                            if leaf_widget._name == "token":
                                token = leaf_widget.get()
                            elif leaf_widget._name == "url":
                                url = leaf_widget.get()
                    if token != "" or url != "":
                        outtext = outtext + f"{token},{url}\n"
                export_file = open(file_path, "w")
                export_file.write(outtext)
                export_file.close()
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    def import_results(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                import_file = open(file_path, "r")
                validate_entry = self.validate_import_var.get()
                count = 0
                for line in import_file.readlines():
                    if count == 0:
                        count = count + 1
                        continue
                    split = line.split(",")
                    entry_res = waifuvault.FileResponse(split[0], split[1])
                    if not validate_entry:
                        self.insert_entry(entry_res)
                        continue
                    try:
                        info = waifuvault.file_info(entry_res.token, True)
                        time.sleep(1)
                        self.insert_entry(entry_res)
                    except:
                        continue
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {e}")

    def create_bucket(self):
        try:
            bucket = waifuvault.create_bucket()
            self.bucket_token_var.delete(0, tk.END)
            self.bucket_token_var.insert(tk.END, bucket.token)
        except Exception as e:
            messagebox.showerror("Error", f"Create bucket failed: {e}")

    def delete_bucket(self):
        try:
            response = messagebox.askyesno("Error", f"Delete will remove bucket and all files.\nAre you sure ?")
            if response:
                token = self.bucket_token_var.get()
                del_bucket = waifuvault.delete_bucket(token)
                self.bucket_token_var.delete(0, tk.END)
                screen_files = self.results_frame.winfo_children()
                frames = [frame for frame in screen_files if isinstance(frame, tk.Frame)]
                for frame in frames:
                    frame.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Delete bucket failed: {e}")

    def get_bucket(self):
        try:
            token = self.bucket_token_var.get()
            bucket = waifuvault.get_bucket(token)
            for file in bucket.files:
                self.insert_entry(file)
        except Exception as e:
            messagebox.showerror("Error", f"Get bucket failed: {e}")

    def show_input_context_menu(self, event):
        self.input_context_menu.post(event.x_root, event.y_root)

    def show_bucket_context_menu(self, event):
        self.bucket_context_menu.post(event.x_root, event.y_root)

    def copy_filename(self, event=None):
        try:
            text_content = self.filename_var.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(text_content)
        except tk.TclError:
            # handle nothing selected
            pass

    def paste_filename(self, event=None):
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

    def copy_bucket(self, event=None):
        try:
            text_content = self.bucket_token_var.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(text_content)
        except tk.TclError:
            # handle nothing selected
            pass

    def paste_bucket(self, event=None):
        try:
            start = self.bucket_token_var.index("sel.first")
            end = self.bucket_token_var.index("sel.last")
            self.bucket_token_var.delete(start, end)
        except tk.TclError:
            # handle nothing selected
            pass
        try:
            text_content = self.root.clipboard_get()
            self.bucket_token_var.insert(tk.INSERT, text_content)
        except tk.TclError:
            # handle nothing in clipboard
            pass

    def render(self, output_frame):
        self.root = output_frame
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="WaifuVault Uploader", font=header_font)
        header_label.pack(anchor="nw")

        self.button_upper_frame = tk.Frame(output_frame)
        self.button_upper_frame.pack(fill=tk.X)
        self.bucket_frame = tk.Frame(output_frame)
        self.bucket_frame.pack(fill=tk.X)
        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X)
        button_lower_frame = tk.Frame(output_frame)
        button_lower_frame.pack(fill=tk.X)

        filename_label = tk.Label(self.button_upper_frame, text="File:")
        filename_label.pack(side="left", padx=(25, 5))
        self.filename_var = tk.Entry(self.button_upper_frame, width=65)
        self.filename_var.bind("<Button-2>", self.show_input_context_menu)
        self.filename_var.bind("<Button-3>", self.show_input_context_menu)
        self.filename_var.pack(side="left", padx=5)
        choosefile_button = tk.Button(self.button_upper_frame, text="Browse", command=self.choose_file)
        choosefile_button.pack(side="left", padx=5)

        bucket_label = tk.Label(self.bucket_frame, text="Bucket:")
        bucket_label.pack(side="left", padx=5)
        self.bucket_token_var = tk.Entry(self.bucket_frame, width=35)
        self.bucket_token_var.bind("<Button-2>", self.show_bucket_context_menu)
        self.bucket_token_var.bind("<Button-3>", self.show_bucket_context_menu)
        self.bucket_token_var.pack(side="left", padx=5)
        create_bucket_button = tk.Button(self.bucket_frame, text="Create Bucket", command=self.create_bucket)
        create_bucket_button.pack(side="left", padx=5)
        get_bucket_button = tk.Button(self.bucket_frame, text="Get Bucket", command=self.get_bucket)
        get_bucket_button.pack(side="left", padx=5)
        delete_bucket_button = tk.Button(self.bucket_frame, text="Delete Bucket", command=self.delete_bucket)
        delete_bucket_button.pack(side="left", padx=5)

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

        self.upload_button = tk.Button(button_lower_frame, text="Upload", command=self.upload_file)
        self.upload_button.pack(side="left", padx=5)
        export_button = tk.Button(button_lower_frame, text="Export Results", command=self.export_results)
        export_button.pack(side="left", padx=5)
        import_button = tk.Button(button_lower_frame, text="Import Results", command=self.import_results)
        import_button.pack(side="left", padx=5)
        self.validate_import_var = tk.BooleanVar(value=False)
        validate_import_flag = tk.Checkbutton(button_lower_frame, text="Validate Import", variable=self.validate_import_var)
        validate_import_flag.pack(side="left", padx=5)

        self.results_frame = tk.Frame(output_frame, pady=15)
        self.results_frame.pack(fill=tk.X)

        self.input_context_menu = tk.Menu(self.button_upper_frame, tearoff=0)
        self.input_context_menu.add_command(label="Copy", command=self.copy_filename)
        self.input_context_menu.add_command(label="Paste", command=self.paste_filename)

        self.bucket_context_menu = tk.Menu(self.bucket_frame, tearoff=0)
        self.bucket_context_menu.add_command(label="Copy", command=self.copy_bucket)
        self.bucket_context_menu.add_command(label="Paste", command=self.paste_bucket)