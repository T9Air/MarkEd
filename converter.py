import re

import tkinter as tk

def parsed_to_readable(parsed_text, textbox):
    split_text = parsed_text.split("(newline)")
    
    line_num = 0
    # Headings
    for line in split_text:
        line_num = line_num + 1
        heading_level = None
        tag_name = None
        
        # Check for heading levels
        for i in range(1, 7):
            if line.startswith(f"(h{i})"):
                heading_level = i
                break
        
        # Insert text with appropriate tag
        if heading_level:
            if (heading_level == 1):
                font_size = 18
            elif (heading_level == 2):
                font_size = 14
            elif (heading_level == 3):
                font_size = 12
            elif (heading_level == 4):
                font_size = 10
            elif (heading_level == 5):
                font_size = 9
            elif (heading_level == 6):
                font_size = 8
            tag_name = f"heading{heading_level}"
            textbox.tag_configure(tag_name, font=("Arial", font_size, "bold"))
            line = line[4:]
        else:
            tag_name = "regular"
            font_size = 10
            textbox.tag_configure(tag_name, font=("Arial", font_size))

        textbox.insert(tk.END, line + "\n", tag_name)
        
        # Bold        
        matches = re.finditer(r"(\(b\))(.+)(\(b\))", line)
        textbox.tag_configure("bold", font=("Arial", font_size, "bold")) 
        for match in matches:
            start, end = match.span()
            start_index = f"{line_num}.{start}"
            end_index = f"{line_num}.{end}"
            delete_start = f"{line_num}.{start + 3}"
            delete_end = f"{line_num}.{end - 3}"
            textbox.tag_add("bold", start_index, end_index)
            textbox.delete(delete_end, end_index)
            textbox.delete(start_index, delete_start)
            
        # Italic
        matches = re.finditer(r"(\(i\))(.+)(\(i\))", line)
        textbox.tag_configure("italic", font=("Arial", font_size, "italic"))
        textbox.tag_configure("bold and italic", font=("Arial", font_size, "italic", "bold"))
        for match in matches:
            start, end = match.span()
            start_index = f"{line_num}.{start}"
            end_index = f"{line_num}.{end}"
            delete_start = f"{line_num}.{start + 3}"
            delete_end = f"{line_num}.{end - 3}"
            textbox.tag_add("italic", start_index, end_index)
            textbox.delete(delete_end, end_index)
            textbox.delete(start_index, delete_start)    