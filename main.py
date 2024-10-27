import tkinter as tk

from tkinter import filedialog

from markdown_parser import parse_markdown

from converter import parsed_to_readable

# Root window configuration
root = tk.Tk()

root.title("MarkEd")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Top frame - save, open file, etc.
top_frame = tk.Frame(root, height=1)
top_frame.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)

top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)

def save():
    save_file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")]) 

    if save_file_path:
        with open(save_file_path, "w") as file:
            file.write(markdown_box.get("1.0", tk.END))

def open_file():
    open_file_path = filedialog.askopenfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
    
    if open_file_path:
        with open(open_file_path, "r") as file:
            text = file.read()
            markdown_box.delete(1.0, tk.END)
            markdown_box.insert(tk.END, text)
            realtext_box.config(state="normal")
            parsed_text = parse_markdown(text)
            parsed_to_readable(parsed_text, realtext_box)
            realtext_box.config(state="disabled")

open_btn = tk.Button(top_frame, text="Open file", height=1, command=open_file)
open_btn.grid(row=0, column=0, sticky="w")

spacer1 = tk.Label(top_frame, width=1)
spacer1.grid(row=0, column=1, sticky="w")

save_btn = tk.Button(top_frame, text="Save file", height=1, command=save)

save_btn.grid(row=0, column=2, sticky="w")

# Markdown frame - markdown text
markdown_frame = tk.Frame(root)
markdown_frame.grid(row=1, column=0, padx=5, pady=5)

markdown_frame.columnconfigure(0, weight=1)
markdown_frame.rowconfigure(0, weight=1)

def update_text(event=None):
    def delayed_update():
        realtext_box.config(state="normal")
        realtext_box.delete(1.0, tk.END)
        markdown_text = markdown_box.get(0.0, tk.END)
        #markdown_lines = markdown_text.splitlines()
        
        #for line in markdown_lines:
        #    realtext_box.insert(tk.END, line + "\n")
        
        parsed_text = parse_markdown(markdown_text)
        parsed_to_readable(parsed_text, realtext_box)
        
        realtext_box.config(state="disabled")
    root.after(1, delayed_update)

markdown_box = tk.Text(markdown_frame, height=15, width=53, yscrollcommand=True)
markdown_box.grid(row=0, column=0, sticky="nsew")
markdown_box.bind("<KeyPress>", update_text)

# Realtext frame - converted text
realtext_frame = tk.Frame(root)
realtext_frame.grid(row=1, column=1, padx=5, pady=5)

realtext_frame.columnconfigure(0, weight=1)
realtext_frame.rowconfigure(0, weight=1)

realtext_box = tk.Text(realtext_frame, height=15, width=53, yscrollcommand=True)
realtext_box.grid(row=0, column=0, sticky="nsew")

root.mainloop()