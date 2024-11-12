import tkinter as tk

from tkinter import filedialog

from markdown_parser import parse_markdown

from converter import parsed_to_readable

import os
# Root window configuration
root = tk.Tk()

root.title("MarkEd")
#root.state('zoomed')
root.configure(bg='gray15')
root.iconbitmap('icon.ico')

# Top frame - save, open file, etc.
top_frame = tk.Frame(root, height=1)
top_frame.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)

file_path = ""

def save():
    current_tab = thetab_manager.get_current_tab()
    if not current_tab.file_path:
        current_tab.file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        if not current_tab.file_path:
            return
    text = markdown_box.get(1.0, tk.END)
    with open(current_tab.file_path, "w") as file:
        file.write(text)

    current_tab.rename(renameto=os.path.basename(current_tab.file_path))


def open_file():
    global file_path
    open_file_path = filedialog.askopenfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
    
    if open_file_path:
        openfiletab = new_tab(thetab_manager)
        with open(open_file_path, "r") as file:
            text = file.read()
            markdown_box.delete(1.0, tk.END)
            markdown_box.insert(tk.END, text)
            realtext_box.config(state="normal")
            realtext_box.delete(1.0, tk.END)
            parsed_text = parse_markdown(text)
            parsed_to_readable(parsed_text, realtext_box)
            realtext_box.config(state="disabled")
        file_path = open_file_path
        openfiletab.textoftab = text
        openfiletab.file_path = open_file_path
        openfiletab.rename(renameto=os.path.basename(open_file_path))

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
        global tabsframe, markdown_box, root
        self.textoftab = ''
        self.file_path = None

        self.tab_manager = tab_manager

        self.tab_frame = tk.Frame(tabsframe)
        self.tab_frame.pack(fill='x', expand=True, side='left')

        self.tab_button = tk.Button(self.tab_frame, text='Untitled File', bg='gray15', fg='white', relief='flat', overrelief='raised', command=self.switch_tab_to_self)
        self.tab_button.pack(fill='x', expand=True, side='left')

        self.tab_delbutton = tk.Button(self.tab_frame, text='❌', bg='gray15', fg='white', relief='flat', overrelief='flat', command=self.delete_tab)
        self.tab_delbutton.pack(side='right')

        self.tab_manager.register_tab(self)
        self.update_delete_buttons()

        self.switch_tab_to_self()

        markdown_box.redraw_line_numbers()
    
    def rename(self, renameto):
        self.tab_button.config(text=renameto)

    def switch_tab_to_self(self):
        self.tab_manager.switch_to_tab(self)
        global markdown_box
        markdown_box.unbind('<KeyRelease>')
        markdown_box.delete(1.0, tk.END)
        root.update()
        markdown_box.insert(1.0, self.textoftab)
        markdown_box.bind('<KeyRelease>', self.update_var, add='+')
        markdown_box.bind("<KeyRelease>", markdown_box.redraw_line_numbers, add='+')
        update_text()

    def activate(self):
        self.tab_button.config(bg='gray30')
        self.tab_delbutton.config(bg='gray30')

    def deactivate(self):
        self.tab_button.config(bg='gray15')
        self.tab_delbutton.config(bg='gray15')
    
    def delete_tab(self):
        self.tab_frame.destroy()
        self.tab_manager.unregister_tab(self)
        self.update_delete_buttons()
        if self.tab_manager.tabs:
            self.tab_manager.tabs[0].switch_tab_to_self()

        markdown_box.redraw_line_numbers()

    def update_var(self, e):
        global markdown_box
        self.textoftab = markdown_box.get(1.0, tk.END)

    def update_delete_buttons(self):
        for tab in self.tab_manager.tabs:
            if len(self.tab_manager.tabs) > 1:
                tab.tab_delbutton.config(state='normal')
            else:
                tab.tab_delbutton.config(state='disabled')

class TabManager:
    def __init__(self):
        self.tabs = []
        self.current_tab = None
    
    def get_numotabs(self):
        return len(self.tabs)

    def register_tab(self, tab):
        self.tabs.append(tab)

    def unregister_tab(self, tab):
        if tab in self.tabs:
            self.tabs.remove(tab)

    def switch_to_tab(self, tab):
        self.current_tab = tab
        for t in self.tabs:
            t.deactivate()
        tab.activate()
    def get_current_tab(self):
        return self.current_tab





global tabsframe
tabsframe = tk.Frame(markdown_frame)
tabsframe.pack(side='top', fill='x')

add_new_tabB = tk.Button(tabsframe, text='+ Create New File', bg='gray30', fg='white', relief='solid', overrelief='solid', command=lambda: new_tab(thetab_manager))
add_new_tabB.pack(fill='x', expand=True, side='left')

markdown_box = CustomText(markdown_frame, insertbackground='white', insertwidth=1, height=30, width=90, yscrollcommand=True, bg='gray30', fg='white', selectbackground='gray15')
markdown_box.pack(side='right', fill='both', expand=True)
markdown_box.bind("<KeyPress>", update_text, add="+")


linenumbers = TextLineNumbers(markdown_frame, width=30)
linenumbers.attach(markdown_box)
linenumbers.pack(side='left', fill='y')

# Realtext frame - converted text
realtext_frame = tk.Frame(root)
realtext_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)


realtext_box = tk.Text(realtext_frame, height=30, width=90, yscrollcommand=True, bg='gray30', fg='white')
realtext_box.pack(fill='both', expand=True)


markdown_box.attach(linenumbers)
markdown_box.bind("<KeyPress>", markdown_box.redraw_line_numbers, add="+")
markdown_box.bind("<MouseWheel>", markdown_box.redraw_line_numbers)
markdown_box.bind("<ButtonRelease-1>", markdown_box.redraw_line_numbers)

markdown_box.linenumbers.redraw()

global thetab_manager
thetab_manager = TabManager()
new_tab(thetab_manager)


realtext_frame.columnconfigure(0, weight=1)
realtext_frame.rowconfigure(0, weight=1)

realtext_box = tk.Text(realtext_frame, height=30, width=90, yscrollcommand=True)
realtext_box.grid(row=0, column=0, sticky="nsew")

root.mainloop()