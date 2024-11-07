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
                1: 22,
                2: 18,
                3: 16,
                4: 14,
                5: 12,
                6: 11
            }.get(heading_level, 14)
            line = line[4:]
        
        if heading_level:
            heading = "h"
            bold = "bold"
        else:
            heading = "r"
            font_size = 14
            bold = ""
        
        # Unordered list
        textbox.tag_configure("bullet", font=("Arial", 14, "bold"))
        if line.startswith("(ul)"):
            textbox.insert(tk.END," " + u"\u2022" + " ", "bullet")
            line = line[4:]
        
        # Bold
        bold_indices = []
        bold_characters = []
        matches = re.finditer(r"(\(b\))(.+?)(\(b\))", line)
        
        end_subtract = 6
        start_subtract = 0
        sr = 0
        er = 0
        
        for match in matches:
            start, end = match.span()
            bold_indices.append(start - start_subtract)
            bold_indices.append(end - end_subtract)
            bold_characters.extend([i for i in range(start + 1 - start_subtract, end + 1 - end_subtract)])
            start_subtract = start_subtract + 6
            end_subtract = end_subtract + 6
            line = line[:start - sr] + line[start + 3 - sr:end - 3 - er] + line[end - er:]
            er += 6
            sr += 6
          
        # Italic
        italic_indices = []
        italic_characters = []
        matches = re.finditer(r"(\(i\))(.+?)(\(i\))", line)
        
        end_subtract = 6
        start_subtract = 0
        sr = 0
        er = 0
        
        for match in matches:
            start, end = match.span()
            italic_indices.append(start - start_subtract)
            italic_indices.append(end - end_subtract)
            for i in range(len(bold_characters)):
                if bold_characters[i - 1] > start - start_subtract:
                    bold_characters[i - 1] -= 3
                if bold_characters[i - 1] > end - end_subtract:
                    bold_characters[i - 1] -= 3
            italic_characters.extend([i for i in range(start + 1 - start_subtract, end + 1 - end_subtract)])
            start_subtract = start_subtract + 6
            end_subtract = end_subtract + 6
            line = line[:start - sr] + line[start + 3 - sr:end - 3 - er] + line[end - er:]
            er += 6
            sr += 6
                        
        # Inline Code Block
        inlinecode_indices = []
        inlinecode_characters = []
        matches = re.finditer(r"(\(ic\))(.+?)(\(ic\))", line)

        end_subtract = 8
        start_subtract = 0
        sr = 0
        er = 0

        for match in matches:
            start, end = match.span()
            inlinecode_indices.append(start - start_subtract)
            inlinecode_indices.append(end - end_subtract)
            for i in range(len(bold_characters)):
                if bold_characters[i - 1] > start - start_subtract:
                    bold_characters[i - 1] -= 4
                if bold_characters[i - 1] > end - end_subtract:
                    bold_characters[i - 1] -= 4
            for i in range(len(italic_characters)):
                if italic_characters[i - 1] > start - start_subtract:
                    italic_characters[i - 1] -= 4
                if italic_characters[i - 1] > end - end_subtract:
                    italic_characters[i - 1] -= 4
            inlinecode_characters.extend([i for i in range(start + 1 - start_subtract, end + 1 - end_subtract)])
            start_subtract = start_subtract + 8
            end_subtract = end_subtract + 8
            line = line[:start - sr] + line[start + 4 - sr:end - 4 - er] + line[end - er:]
            er += 8
            sr += 8

        # Adding characters to textbox
        char_num = 0 # Create a variable to store what number character on the line it is up to
        for char in line:
            char_num = char_num + 1
            
            if char_num in inlinecode_characters:
                backgrounds = "lightgray"
            else:
                backgrounds = "white"
            
            if char_num in bold_characters or heading == "h":
                bold = ",bold"
            else:
                bold = ","
            
            if char_num in italic_characters:
                italic = ",italic"
            else:
                italic = ","
            
            if char_num in inlinecode_characters:
                backgrounds = "gray40"
                if heading == "r":
                    bold = ","
                else:
                    bold = ",bold"
                italic = ","
            else:
                backgrounds = "gray30"
            
            # Tag name is a combination of all changes
            tag_name = heading + str(font_size) + bold + italic + "," + backgrounds
            
            if bold == ",bold" and italic == ",italic":
                textbox.tag_configure(tag_name, font=("Arial", font_size, "bold", "italic"), background = backgrounds)
            elif bold == ",bold":
                textbox.tag_configure(tag_name, font=("Arial", font_size, "bold"), background = backgrounds)
            elif italic == ",italic":
                textbox.tag_configure(tag_name, font=("Arial", font_size, "italic"), background = backgrounds)
            else:
                textbox.tag_configure(tag_name, font=("Arial", font_size), background = backgrounds)
            
            textbox.insert(tk.END, char, tag_name)

        textbox.insert(tk.END, "\n")