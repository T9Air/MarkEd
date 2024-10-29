import re

import tkinter as tk

def parsed_to_readable(parsed_text, textbox):
    split_text = parsed_text.split("(newline)")
    for line in split_text:
        heading_level = None
        font_size = None
        
        for i in range(1, 7):
            if line.startswith(f"(h{i})"):
                heading_level = i
                break
        
        if heading_level:
            font_size = {
                1: 18,
                2: 14,
                3: 12,
                4: 10,
                5: 9,
                6: 8
            }.get(heading_level, 10)
            line = line[4:]
        
        if heading_level:
            heading = "h"
        else:
            heading = "r"
            font_size = 10
                             
        for char in line:
            textbox.insert(tk.END, char)
            print(font_size)
            
        textbox.insert(tk.END, "\n")