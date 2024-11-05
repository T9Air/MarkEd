import tkinter as tk

from tkinter import filedialog

from markdown_parser import parse_markdown

from converter import parsed_to_readable

# Root window configuration
root = tk.Tk()

root.title("MarkEd")
root.configure(bg='gray15')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Top frame - save, open file, etc.
top_frame = tk.Frame(root, height=1, bg='gray15')
top_frame.pack(fill='x', padx=10, pady=10)

file_path = ""

def save():
    global file_path
    if file_path == "":
        save_file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")]) 

        if save_file_path:
            with open(save_file_path, "w") as file:
                file.write(markdown_box.get("1.0", tk.END))
            file_path = save_file_path
    else:
        with open(file_path, "w") as file:
            file.write(markdown_box.get("1.0", tk.END))

def open_file():
    global file_path
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
        file_path = open_file_path

open_btn = tk.Button(top_frame, text="Open file", height=1, command=open_file, relief='flat', overrelief='solid')
open_btn.grid(row=0, column=0, padx=5, sticky='w')

save_btn = tk.Button(top_frame, text="Save file", height=1, command=save, relief='flat', overrelief='solid')
save_btn.grid(row=0, column=1, padx=5, sticky='w')

# Markdown frame - markdown text
markdown_frame = tk.Frame(root, bg='red')
markdown_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)


def update_text(event=None):
    def delayed_update():
        realtext_box.config(state="normal")
        realtext_box.delete(1.0, tk.END)
        markdown_text = markdown_box.get(0.0, tk.END)
        
        parsed_text = parse_markdown(markdown_text)
        parsed_to_readable(parsed_text, realtext_box)
        
        realtext_box.config(state="disabled")
    root.after(1, delayed_update)

markdown_box = tk.Text(markdown_frame, height=30, width=90, yscrollcommand=True, bg='gray30', fg='white')
markdown_box.grid(row=0, column=0, sticky="nsew")
markdown_box.bind("<KeyPress>", update_text)

# Realtext frame - converted text
realtext_frame = tk.Frame(root)
realtext_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

realtext_frame.columnconfigure(0, weight=1)
realtext_frame.rowconfigure(0, weight=1)

realtext_box = tk.Text(realtext_frame, height=30, width=90, yscrollcommand=True, bg='gray30', fg='white')
realtext_box.grid(row=0, column=0, sticky="nsew")

root.mainloop()