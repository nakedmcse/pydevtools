# JSON pretty print module
import tkinter as tk
from tkinter import font, filedialog, messagebox
import json

from devmodules import basedevtools as base


class json_prettyprint(base.basedevtools):
    display_name = "JSON Pretty Printer"
    category = "Format tools"
    input_text = ""
    input_text_frame = None
    output_text = ""
    output_text_frame = None
    indent_var = None
    sort_var = None

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.input_text = file.read()
                    self.input_text_frame.delete(1.0, tk.END)
                    self.input_text_frame.insert(tk.END, self.input_text[:1048576])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.output_text)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def convert_json(self):
        if len(self.input_text) > 1048576:
            self.input_text = self.input_text_frame.get(1.0, tk.END)[:-1] + self.input_text[1048577:]
        else:
            self.input_text = self.input_text_frame.get(1.0, tk.END)
        try:
            obj = json.loads(self.input_text)
            indent_level = None if self.indent_var.get() == "minify" else int(self.indent_var.get())
            self.output_text = json.dumps(obj, indent=indent_level, sort_keys=self.sort_var.get())
            self.output_text_frame.config(state=tk.NORMAL)
            self.output_text_frame.delete(1.0, tk.END)
            self.output_text_frame.insert(tk.END, self.output_text[:1048576])
            self.output_text_frame.config(state=tk.DISABLED)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON")

    def render(self, output_frame):
        self.input_text = ""
        self.output_text = ""
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="JSON Pretty Printer", font=header_font)
        header_label.pack(anchor="nw")

        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X, pady=5)

        load_button = tk.Button(button_frame, text="Load", command=self.load_file)
        load_button.pack(side="left", padx=5)

        indent_label = tk.Label(button_frame, text="Indent:")
        indent_label.pack(side="left")
        self.indent_var = tk.StringVar(value="4")
        indent_menu = tk.OptionMenu(button_frame, self.indent_var, "4", "3", "2", "1", "0", "minify")
        indent_menu.config(width=6)
        indent_menu.pack(side="left", padx=5)

        self.sort_var = tk.BooleanVar(value=False)
        sort_flag = tk.Checkbutton(button_frame, text="Sort", variable=self.sort_var)
        sort_flag.pack(side="left", padx=5)

        convert_button = tk.Button(button_frame, text="Convert", command=self.convert_json)
        convert_button.pack(side="left", padx=5)

        save_button = tk.Button(button_frame, text="Save", command=self.save_file)
        save_button.pack(side="left", padx=5)

        self.input_text_frame = tk.Text(output_frame, width=40)
        self.output_text_frame = tk.Text(output_frame, state=tk.DISABLED, width=40)
        self.input_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
        self.output_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
