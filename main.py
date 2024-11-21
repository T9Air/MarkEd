import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from markdown_parser import parse_markdown
from converter import parsed_to_readable
import os
import database_host

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
        self.configure(bg=color1, highlightthickness=0)

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
            self.create_text(2, y, anchor="nw", text=linenum, fill=color3)
            i = self.textwidget.index("%s+1line" % i)
            self.configure(bg=color1, highlightthickness=0)

class new_tab:
    def __init__(self, tab_manager):
        global tabsframe, markdown_box, root
        self.textoftab = ''
        self.file_path = None

        self.tab_manager = tab_manager

        self.tab_frame = tk.Frame(tabsframe, bg='grey15')
        self.tab_frame.pack(fill='both', expand=True, side='left')

        self.tab_button = tk.Label(self.tab_frame, text='Untitled File', bg=color2, fg=color3, relief='flat')
        self.tab_button.pack(fill='x', expand=True, side='left')
        self.tab_button.bind('<ButtonPress-1>', self.switch_tab_to_self)

        self.tab_delbutton = tk.Label(self.tab_frame, text='❌', bg=color2, fg=color3, relief='flat')
        self.tab_delbutton.pack(side='right')
        self.tab_delbutton.bind('<ButtonPress-1>', self.delete_tab)
        self.tab_delbutton.bind('<Enter>', self.switch_to_x)
        self.tab_delbutton.bind('<Leave>', self.update_saved)

        self.tab_manager.register_tab(self)
        self.update_delete_buttons()

        self.switch_tab_to_self()

        markdown_box.redraw_line_numbers()

    def rename(self, renameto):
        self.tab_button.config(text=renameto)

    def switch_to_x(self, e):
        self.tab_delbutton.config(text='❌')

    def switch_tab_to_self(self, e=None):
        self.tab_manager.switch_to_tab(self)
        global markdown_box
        markdown_box.unbind('<KeyRelease>')
        markdown_box.delete(1.0, tk.END)
        root.update()
        markdown_box.insert(1.0, self.textoftab)
        markdown_box.bind('<KeyRelease>', self.update_var, add='+')
        markdown_box.bind("<KeyRelease>", markdown_box.redraw_line_numbers, add='+')
        markdown_box.bind("<KeyRelease>", self.update_saved, add='+')
        update_text()

    def update_saved(self, e):        
        if self.file_path is None:
            self.tab_delbutton.config(state='normal')
            if self.textoftab.strip() != "":
                self.tab_delbutton.config(text='\u2B24')
            else:
                self.tab_delbutton.config(text='❌')
        else:
            with open(self.file_path, "r") as file:
                saved_text = file.read()
                
            if saved_text.strip() != markdown_box.get(1.0, tk.END).strip():
                self.tab_delbutton.config(text='\u2B24')
            else:
                self.tab_delbutton.config(text='❌')

    def activate(self):
        self.tab_frame.config(bg=color1)
        self.tab_button.config(bg=color1, fg=color3)
        self.tab_delbutton.config(bg=color1, fg=color3)

    def deactivate(self):
        self.tab_frame.config(bg=color2)
        self.tab_button.config(bg=color2, fg=color3)
        self.tab_delbutton.config(bg=color2, fg=color3)
    
    def delete_tab(self, e=None):
        if self.file_path is None:
            if self.textoftab.strip() != "":
                savechanges = tk.messagebox.askyesnocancel('Are you sure?', 'Do you want to save changes?')
                if savechanges is True:
                    save()
                    self.tab_frame.destroy()
                    self.tab_manager.unregister_tab(self)
                    self.update_delete_buttons()
                    if self.tab_manager.tabs:
                        self.tab_manager.tabs[0].switch_tab_to_self()

                    markdown_box.redraw_line_numbers()
                    if len(self.tab_manager.tabs) == 0:
                        new_tab(thetab_manager)
                elif savechanges is False:
                    self.tab_frame.destroy()
                    self.tab_manager.unregister_tab(self)
                    self.update_delete_buttons()
                    if self.tab_manager.tabs:
                        self.tab_manager.tabs[0].switch_tab_to_self()

                    markdown_box.redraw_line_numbers()
                    if len(self.tab_manager.tabs) == 0:
                        new_tab(thetab_manager)
            else:
                self.tab_frame.destroy()
                self.tab_manager.unregister_tab(self)
                self.update_delete_buttons()
                if self.tab_manager.tabs:
                    self.tab_manager.tabs[0].switch_tab_to_self()

                markdown_box.redraw_line_numbers()
                if len(self.tab_manager.tabs) == 0:
                    new_tab(thetab_manager)
        else:
            with open(self.file_path, "r") as file:
                saved_text = file.read()
            if saved_text.strip() != self.textoftab.strip():
                savechanges = tk.messagebox.askyesnocancel('Are you sure?', 'Do you want to save changes?')
                if savechanges is True:
                    save()
                    self.tab_frame.destroy()
                    self.tab_manager.unregister_tab(self)
                    self.update_delete_buttons()
                    if self.tab_manager.tabs:
                        self.tab_manager.tabs[0].switch_tab_to_self()

                    markdown_box.redraw_line_numbers()
                    if len(self.tab_manager.tabs) == 0:
                        new_tab(thetab_manager)
                elif savechanges is False:
                    self.tab_frame.destroy()
                    self.tab_manager.unregister_tab(self)
                    self.update_delete_buttons()
                    if self.tab_manager.tabs:
                        self.tab_manager.tabs[0].switch_tab_to_self()

                    markdown_box.redraw_line_numbers()
                    if len(self.tab_manager.tabs) == 0:
                        new_tab(thetab_manager)
            else:
                self.tab_frame.destroy()
                self.tab_manager.unregister_tab(self)
                self.update_delete_buttons()
                if self.tab_manager.tabs:
                    self.tab_manager.tabs[0].switch_tab_to_self()

                markdown_box.redraw_line_numbers()
                if len(self.tab_manager.tabs) == 0:
                    new_tab(thetab_manager)

    def update_var(self, e):
        global markdown_box
        self.textoftab = markdown_box.get(1.0, tk.END)

    def update_delete_buttons(self):
        for tab in self.tab_manager.tabs:
            if len(self.tab_manager.tabs) > 1:
                tab.tab_delbutton.config(state='normal')
            else:
                tab.tab_delbutton.config(state='normal')

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

    def reset_tab_colors(self):
        for tab in self.tabs:
            tab.deactivate()
            if self.current_tab:
                self.current_tab.activate()

def save(e=None):
    current_tab = thetab_manager.get_current_tab()
    if not current_tab.file_path:
        current_tab.file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        if not current_tab.file_path:
            return
    text = markdown_box.get(1.0, tk.END)
    with open(current_tab.file_path, "w") as file:
        file.write(text)
    root.update()
    current_tab.rename(renameto=os.path.basename(current_tab.file_path))
    current_tab.update_saved('')

def open_file(e=None):
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
            parsed_text, escape_positions = parse_markdown(text)
            parsed_to_readable(parsed_text, escape_positions, realtext_box)
            realtext_box.config(state="disabled")
        file_path = open_file_path
        openfiletab.textoftab = text
        openfiletab.file_path = open_file_path
        openfiletab.rename(renameto=os.path.basename(open_file_path))

def update_text(event=None):
    def delayed_update():
        realtext_box.config(state="normal")
        realtext_box.delete(1.0, tk.END)
        markdown_text = markdown_box.get(0.0, tk.END)
        
        parsed_text, escape_positions = parse_markdown(markdown_text)
        parsed_to_readable(parsed_text, escape_positions, realtext_box)
        
        realtext_box.config(state="disabled")
    root.after(1, delayed_update)

def update_themebuttons():
    if database_host.get_setting('theme') == 'dark':
        set_themedarkB.configure(relief='solid', font=('Calibri', 15, 'bold'))
        set_themelightB.configure(relief='flat', font=('Calibri', 15))
    if database_host.get_setting('theme') == 'light':
        set_themelightB.configure(relief='solid', font=('Calibri', 15, 'bold'))
        set_themedarkB.configure(relief='flat', font=('Calibri', 15))

def settings_fun():
    global settings_frame, set_themedarkB, set_themelightB, set_headerL, set_themeL
    settings_frame = tk.Frame(root, bg=color2)
    settings_frame.place(relx=.5, rely=.5)
    set_headerL = tk.Label(settings_frame, text='Settings', font=('Calibri', 20, 'bold'), bg=color2, fg=color3)
    set_headerL.grid(row=0, column=0, columnspan=3)

    set_themeL = tk.Label(settings_frame, text='Theme', font=('Calibri', 15, 'bold'), bg=color2, fg=color3)
    set_themeL.grid(row=1, column=0, pady=10)

    set_themelightB = tk.Button(settings_frame, text='Light Theme', font=('Calibri', 15), bg=color2, fg=color3, relief='flat', overrelief='solid', command=lambda: (database_host.setting_configure('theme', 'light'), update_themebuttons(), update_theme()))
    set_themelightB.grid(row=1, column=1, pady=10, padx=5)
    if database_host.get_setting('theme') == 'light':
        set_themelightB.configure(relief='solid', font=('Calibri', 15, 'bold'))

    set_themedarkB = tk.Button(settings_frame, text='Dark Theme', font=('Calibri', 15), bg=color2, fg=color3, relief='flat', overrelief='solid', command=lambda: (database_host.setting_configure('theme', 'dark'), update_themebuttons(), update_theme()))
    set_themedarkB.grid(row=1, column=2, pady=10, padx=5)
    if database_host.get_setting('theme') == 'dark':
        set_themedarkB.configure(relief='solid', font=('Calibri', 15, 'bold'))

    set_headerL = tk.Label(settings_frame, text='See changes upon reopening', font=('Calibri', 10), bg=color2, fg=color3)

    set_close = tk.Button(settings_frame, text='Close Settings', font=('Calibri', 10), bg=color2, fg=color3, command=lambda: settings_frame.destroy())
    set_close.grid(row=3, column=0, pady=10, columnspan=3)

def update_theme():
    global color1, color2, color3
    color1 = 'gray30'
    color2 = 'gray15'
    color3 = 'white'
    if database_host.get_setting('theme') == 'light':
        color1 = 'gray85'
        color2 = 'gray70'
        color3 = 'black'

    # Root
    root.configure(bg=color2)
    # Settings
    settings_frame.configure(bg=color2)
    set_themedarkB.configure(bg=color2, fg=color3)
    set_themelightB.configure(bg=color2, fg=color3)
    set_headerL.configure(bg=color2, fg=color3)
    set_themeL.configure(bg=color2, fg=color3)
    # Top Frame
    top_frame.configure(bg=color2)
    # Markdown Frame
    markdown_frame.configure(bg=color2)
    # Tabs Frame
    tabsframe.configure(bg=color2)
    add_new_tabB.configure(bg=color1, fg=color3)
    # Markdown Box
    markdown_frame.configure(bg=color1)
    markdown_box.configure(insertbackground=color3, bg=color1, fg=color3, selectbackground=color2)
    linenumbers.redraw()
    # Real text
    realtext_box.configure(bg=color1, fg=color3, selectbackground=color1)
    # Tabs
    thetab_manager.reset_tab_colors()

def setup_ui():
    global root, top_frame, markdown_frame, tabsframe, add_new_tabB
    global markdown_box, linenumbers, realtext_frame, realtext_box, thetab_manager
    global color1, color2, color3, file_path

    # Initialize colors based on theme
    color1 = 'gray30'
    color2 = 'gray15'
    color3 = 'white'
    if database_host.get_setting('theme') == 'light':
        color1 = 'gray85'
        color2 = 'gray70'
        color3 = 'black'

    # Initialize file path
    file_path = ""

    # Root window configuration
    root = tk.Tk()
    root.title("MarkEd")
    root.iconbitmap('icon.ico')
    root.configure(bg=color2)

    # Top Frame
    top_frame = tk.Frame(root, height=1, bg=color2)
    top_frame.pack(fill='x', padx=10, pady=10)

    open_btn = tk.Button(top_frame, text="Open file", height=1, command=open_file, relief='flat', overrelief='solid')
    open_btn.grid(row=0, column=0, padx=5, sticky='w')

    save_btn = tk.Button(top_frame, text="Save file", height=1, command=save, relief='flat', overrelief='solid')
    save_btn.grid(row=0, column=1, padx=5, sticky='w')

    settingsB = tk.Button(top_frame, text="\u2699 Settings", height=1, relief='flat', overrelief='solid', command=settings_fun)
    top_frame.grid_columnconfigure(0, weight=0)
    top_frame.grid_columnconfigure(1, weight=0)
    top_frame.grid_columnconfigure(2, weight=1)
    settingsB.grid(row=0, column=2, padx=5, sticky='e')

    # Markdown Frame
    markdown_frame = tk.Frame(root, bg=color1)
    markdown_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

    # Tabs Frame
    tabsframe = tk.Frame(markdown_frame, height=30, bg=color2)
    tabsframe.pack(side='top', fill='x')
    tabsframe.pack_propagate(False)

    add_new_tabB = tk.Button(tabsframe, text='+ Create New File', bg=color1, fg=color3, relief='flat', overrelief='solid', command=lambda: new_tab(thetab_manager))
    add_new_tabB.pack(fill='both', expand=True, side='left', padx=1, pady=0)

    # Markdown Box
    '''markdown_box = CustomText(markdown_frame, insertbackground=color3, insertwidth=1, tabs='    ', height=30, width=90, yscrollcommand=True, bg=color1, fg=color3, selectbackground=color2, font=('Consolas', 11))
    markdown_box.pack(side='right', fill='both', expand=True)

    linenumbers = TextLineNumbers(markdown_frame, width=30)
    linenumbers.attach(markdown_box)
    linenumbers.pack(side='left', fill='y')'''

    # -------------------- Markdown Box --------------------
    global markdown_box, linenumbers
    markdown_box = CustomText(markdown_frame, insertbackground=color3, insertwidth=1, tabs='    ', height=30, width=90, yscrollcommand=True, bg=color1, fg=color3, selectbackground=color2, font=('Consolas', 11))
    linenumbers = TextLineNumbers(markdown_frame, width=30)
    linenumbers.attach(markdown_box)
    linenumbers.pack(side='left', fill='y')
    markdown_box.pack(side='left', fill='both', expand=True)

    scrollbar = tk.Scrollbar(markdown_frame, command=markdown_box.yview, bg=color2)
    scrollbar.pack(side='right', fill='y', expand=True)
    markdown_box.config(yscrollcommand=scrollbar.set)

        # >> Markdown Box Bindings <<
    markdown_box.bind("<KeyPress>", update_text, add="+")
    markdown_box.attach(linenumbers)
    markdown_box.bind("<KeyPress>", markdown_box.redraw_line_numbers, add="+")
    markdown_box.bind("<MouseWheel>", markdown_box.redraw_line_numbers)
    markdown_box.bind("<ButtonRelease-1>", markdown_box.redraw_line_numbers, add='+')
    scrollbar.bind("<B1-Motion>", markdown_box.redraw_line_numbers, add='+')
    markdown_box.linenumbers.redraw()

    # Realtext frame
    realtext_frame = tk.Frame(root)
    realtext_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

    realtext_box = tk.Text(realtext_frame, height=30, width=90, yscrollcommand=True, bg=color1, fg=color3, selectbackground=color1)
    realtext_box.pack(fill='both', expand=True)

    # Initialize Tab Manager
    thetab_manager = TabManager()
    new_tab(thetab_manager)

    # Global Bindings
    root.bind('<Control-s>', save)
    root.bind('<Control-o>', open_file)

def main():
    """Main function to initialize and run the Markdown editor application."""
    setup_ui()
    root.mainloop()

if __name__ == "__main__":
    main()