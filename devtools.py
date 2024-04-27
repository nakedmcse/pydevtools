import tkinter as tk
from tkinter import ttk

from devmodules import basedevtools as base


def on_menu_select(event):
    selected_item = tree.focus()
    item_text = tree.item(selected_item, 'text')
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"You selected: {item_text}\n")
    output_text.config(state=tk.DISABLED)


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
for devmod in module_classes:
    categories = add_dev_module(tree, devmod, categories)

# Create the output area
output_frame = ttk.Frame(pane, width=500)
output_text = tk.Text(output_frame, state=tk.DISABLED)
output_text.pack(expand=True, fill=tk.BOTH)

pane.add(menu_frame, weight=1)
pane.add(output_frame, weight=3)

main_window.mainloop()
