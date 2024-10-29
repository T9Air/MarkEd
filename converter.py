import re

import tkinter as tk

def parsed_to_readable(parsed_text, textbox):
    split_text = parsed_text.split("(newline)")
    for line in split_text:
        font_size = None
        
        # Headings
        heading_level = None
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
            bold = "bold"
        else:
            heading = "r"
            font_size = 10
            bold = ""
        
        # Bold
        bold_indices = []
        bold_characters = []
        matches = re.finditer(r"(\(b\))(.+)(\(b\))", line)
        
        for match in matches:
            start, end = match.span()
            bold_indices.append((start, end))
            bold_characters.extend([i for i in range(start, end + 1)])
            
        # Adding characters to textbox
        char_num = 0 # Create a variable to store what number character on the line it is up to
        for char in line:
            char_num = char_num + 1
            
            if char_num in bold_characters:
                bold = "bold"
            
            # Tag name is a combination of all changes
            tag_name = heading + "," + str(font_size) + "," + bold
            textbox.tag_configure(tag_name, font=("Arial", font_size, bold))
            textbox.insert(tk.END, char, tag_name)
            
        textbox.insert(tk.END, "\n")