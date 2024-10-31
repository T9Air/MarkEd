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
            bold_characters.extend([i for i in range(start + 1, end + 1)])
            
        # Italic
        italic_indices = []
        italic_characters = []
        matches = re.finditer(r"(\(i\))(.+)(\(i\))", line)
        
        for match in matches:
            start, end = match.span()
            italic_indices.append((start, end))
            italic_characters.extend([i for i in range(start + 1, end + 1)])

        # Adding characters to textbox
        char_num = 0 # Create a variable to store what number character on the line it is up to
        for char in line:
            # char_num = char_num + 1
            
            # if char_num in bold_characters or heading == "h":
            #     bold = ",bold"
            # else:
            #     bold = ","
            
            # if char_num in italic_characters:
            #     italic = ",italic"
            # else:
            #     italic = ","
            
            # # Tag name is a combination of all changes
            # tag_name = heading + str(font_size) + bold + italic
            
            # if bold == ",bold" and italic == ",italic":
            #     textbox.tag_configure(tag_name, font=("Arial", font_size, "bold", "italic"))
            # elif bold == ",bold":
            #     textbox.tag_configure(tag_name, font=("Arial", font_size, "bold"))
            # elif italic == ",italic":
            #     textbox.tag_configure(tag_name, font=("Arial", font_size, "italic"))
            # else:
            #     textbox.tag_configure(tag_name, font=("Arial", font_size))
            
            # textbox.insert(tk.END, char, tag_name)
            textbox.insert(tk.END, char)

        textbox.insert(tk.END, "\n")