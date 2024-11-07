import tkinter as tk

from tkinter import filedialog

from markdown_parser import parse_markdown

from converter import parsed_to_readable

# Root window configuration
root = tk.Tk()

root.title("MarkEd")
#root.state('zoomed')
root.configure(bg='gray15')

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
markdown_frame = tk.Frame(root, bg='gray30')
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

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.linenumbers = None

    def attach(self, linenumbers):
        self.linenumbers = linenumbers

    def redraw_line_numbers(self, *args):
        self.linenumbers.redraw()

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.configure(bg='gray30', highlightthickness=0)

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill='white')
            i = self.textwidget.index("%s+1line" % i)

class new_tab:
    def __init__(self, tab_manager):
        global tabsframe
        self.tab_manager = tab_manager

        self.tab_frame = tk.Frame(tabsframe)
        self.tab_frame.pack(fill='x', expand=True, side='left')

        self.tab_button = tk.Button(self.tab_frame, text='Untitled File', bg='gray15', fg='white', relief='flat', overrelief='raised', command=lambda: self.switch_tab_to_self())
        self.tab_button.pack(fill='x', expand=True, side='left')

        self.tab_delbutton = tk.Button(self.tab_frame, text='🗑️', bg='gray15', fg='white', relief='flat', overrelief='flat', command=lambda: self.delete_tab())
        self.tab_delbutton.pack(side='right')

        self.tab_manager.register_tab(self)

        self.switch_tab_to_self()

    def switch_tab_to_self(self):
        print(f'Tab Switched to {self}')
        self.tab_manager.switch_to_tab(self)

    def activate(self):
        self.tab_button.config(bg='gray30')
        self.tab_delbutton.config(bg='gray30')

    def deactivate(self):
        self.tab_button.config(bg='gray15')
        self.tab_delbutton.config(bg='gray15')
    
    def delete_tab(self):
        self.tab_frame.destroy()
        self.tab_manager.unregister_tab(self)

class TabManager:
    def __init__(self):
        self.tabs = []

    def register_tab(self, tab):
        self.tabs.append(tab)
    def unregister_tab(self, tab):
        if tab in self.tabs:
            self.tabs.remove(tab)

    def switch_to_tab(self, tab):
        for t in self.tabs:
            t.deactivate()
        tab.activate()




global tabsframe
tabsframe = tk.Frame(markdown_frame)
tabsframe.pack(side='top', fill='x')

add_new_tabB = tk.Button(tabsframe, text='+ Create New File', bg='gray30', fg='white', relief='solid', overrelief='solid', command=lambda: new_tab(thetab_manager))
add_new_tabB.pack(fill='x', expand=True, side='left')

markdown_box = CustomText(markdown_frame, insertbackground='white', insertwidth=1, height=30, width=90, yscrollcommand=True, bg='gray30', fg='white')
markdown_box.pack(side='right', fill='both', expand=True)
markdown_box.bind("<KeyPress>", update_text)


linenumbers = TextLineNumbers(markdown_frame, width=30)
linenumbers.attach(markdown_box)
linenumbers.pack(side='left', fill='y')

# Realtext frame - converted text
realtext_frame = tk.Frame(root)
realtext_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)


realtext_box = tk.Text(realtext_frame, height=30, width=90, yscrollcommand=True, bg='gray30', fg='white')
realtext_box.pack(fill='both', expand=True)


markdown_box.attach(linenumbers)
markdown_box.bind("<KeyPress>", markdown_box.redraw_line_numbers)
markdown_box.bind("<KeyRelease>", markdown_box.redraw_line_numbers)
markdown_box.bind("<MouseWheel>", markdown_box.redraw_line_numbers)
markdown_box.bind("<ButtonRelease-1>", markdown_box.redraw_line_numbers)

markdown_box.linenumbers.redraw()

global thetab_manager
thetab_manager = TabManager()
new_tab(thetab_manager)




root.mainloop()
