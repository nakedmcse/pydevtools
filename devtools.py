import tkinter as tk
from tkinter import ttk

from devmodules import basedevtools as base
from devmodules import json_prettyprint, xml_prettyprint, jpg_exif, image_compressor, youtube_dl, waifuvault

def on_menu_select(event):
    global output_frame, pane
    selected_item = tree.focus()
    item_text = tree.item(selected_item, 'text')
    output_frame.destroy()
    output_frame = ttk.Frame(pane)
    pane.add(output_frame, weight=3)
    if item_text in modules:
        modules[item_text].render(output_frame)
    else:
        output_text = tk.Text(output_frame, state=tk.DISABLED)
        output_text.pack(expand=True, fill=tk.BOTH)


def add_dev_module(tree: any, devmod: any, categories: any):
    if devmod.category in categories:
        tree.insert(categories[devmod.category], tk.END, text=devmod.display_name)
    else:
        cat_id = tree.insert('', tk.END, text=devmod.category, open=False)
        categories[devmod.category] = cat_id
        tree.insert(cat_id, tk.END, text=devmod.display_name)
    return categories


main_window = tk.Tk()
main_window.title("Dev Tools")
main_window.geometry("1024x600")

# Create PanedWindow
pane = ttk.PanedWindow(main_window, orient=tk.HORIZONTAL)
pane.pack(fill=tk.BOTH, expand=True)

# Create the tree menu
menu_frame = ttk.Frame(pane, width=200)
tree = ttk.Treeview(menu_frame)
tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)
tree.bind('<<TreeviewSelect>>', on_menu_select)

module_classes = base.basedevtools.__subclasses__()
categories = {}
modules = {}
for devmod in sorted(module_classes, reverse=True, key=lambda cls: cls.__name__):
    categories = add_dev_module(tree, devmod, categories)
    modules[devmod.display_name] = devmod(devmod.display_name, devmod.category)

# Create the output area
output_frame = ttk.Frame(pane, width=500)
output_text = tk.Text(output_frame, state=tk.DISABLED)
output_text.pack(expand=True, fill=tk.BOTH)

pane.add(menu_frame, weight=1)
pane.add(output_frame, weight=3)

main_window.mainloop()
