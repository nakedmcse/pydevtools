# JSON pretty print module
import tkinter as tk
from tkinter import font, filedialog, messagebox
import json

from devmodules import basedevtools as base


class json_prettyprint(base.basedevtools):
    display_name = "JSON Pretty Printer"
    category = "Format tools"
    input_text_frame = None
    output_text_frame = None
    indent_var = None

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.input_text_frame.delete(1.0, tk.END)
                    self.input_text_frame.insert(tk.END, file.read())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.output_text_frame.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def convert_json(self):
        try:
            obj = json.loads(self.input_text_frame.get(1.0, tk.END))
            formatted_json = json.dumps(obj, indent=int(self.indent_var.get()))
            self.output_text_frame.config(state=tk.NORMAL)
            self.output_text_frame.delete(1.0, tk.END)
            self.output_text_frame.insert(tk.END, formatted_json)
            self.output_text_frame.config(state=tk.DISABLED)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON")

    def render(self, output_frame):
        header_font = font.Font(size=14, weight="bold")
        header_label = tk.Label(output_frame, text="JSON Pretty Printer", font=header_font)
        header_label.pack(anchor="nw")

        button_frame = tk.Frame(output_frame)
        button_frame.pack(fill=tk.X)

        load_button = tk.Button(button_frame, text="Load", command=self.load_file)
        load_button.pack(side="left", padx=5)

        self.indent_var = tk.StringVar(value="4")
        indent_menu = tk.OptionMenu(button_frame, self.indent_var, "4", "3", "2", "1", "0")
        indent_menu.pack(side="left", padx=5)

        convert_button = tk.Button(button_frame, text="Convert", command=self.convert_json)
        convert_button.pack(side="left", padx=5)

        save_button = tk.Button(button_frame, text="Save", command=self.save_file)
        save_button.pack(side="left", padx=5)

        input_text_frame = tk.Text(output_frame, width=40)
        output_text_frame = tk.Text(output_frame, state=tk.DISABLED, width=40)
        input_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
        output_text_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
