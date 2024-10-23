import re

import tkinter as tk

def parsed_to_readable(parsed_text, textbox):
    split_text = parsed_text.split("(newline)")
    for line in split_text:
        textbox.insert(tk.END, line + "\n")