import re

def parse_markdown(markdown_text):
    lines = markdown_text.splitlines()
    escape_positions = []    
    i = 0
    
    for line in lines:
        # Escape any characters that would be a parsed output
        line_escape_pos = []
        
        line, line_escape_pos = escape_parsed(line, line_escape_pos)
        
        # Parse Markdown
        # Markdown code for the beggining of the line
        if line.startswith("###### "): # Heading 6
            line = "(h6)" + line[7:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 3
        elif line.startswith("##### "): # Heading 5
            line = "(h5)" + line[6:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 2
        elif line.startswith("#### "): # Heading 4
            line = "(h4)" + line[5:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 1
        elif line.startswith("### "): # Heading 3
            line = "(h3)" + line[4:]
        elif line.startswith("## "): # Heading 2
            line = "(h2)" + line[3:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] += 1
        elif line.startswith("# "): # Heading 1
            line = "(h1)" + line[2:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] += 2
        elif line.startswith("> "): # Blockquote
            line = "(bq)" + line[2:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] += 2
        elif line.startswith("- [x] "): # Checked Box
            line = "(checked)" + line[6:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] += 3
        elif line.startswith("- [ ] "): # Unchecked Box
            line = "(unchecked)" + line[6:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] += 5
        elif line.startswith("- "): # Unordered List
            line = "(ul)" + line[2:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] += 2
        elif re.match(r"^\d+\. ", line): # Ordered List
            match = re.match(r"^\d+\. ", line)
            line = "(ol)" + line[match.end():]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= match.end() - 4
        
        # Inline Markdown Code
        # Bold
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)\*\*(?=[^\*])(.+?)(?<!\\)\*\*", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(b)" + match.group(1) + "(b)" + line[end:]
                for j in range(len(line_escape_pos)):
                    if line_escape_pos[j - 1] > end:
                        line_escape_pos[j - 1] += 2
                    if line_escape_pos[j - 1] > start:
                        line_escape_pos[j - 1] += 1
                    
        # Italic
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)\*(?=[^\*])(.+?)(?<!\\)\*", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(i)" + match.group(1) + "(i)" + line[end:]
                for j in range(len(line_escape_pos)):
                    if line_escape_pos[j - 1] > end:
                        line_escape_pos[j - 1] += 4
                    if line_escape_pos[j - 1] > start:
                        line_escape_pos[j - 1] += 2
        
        # Inline Code
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)`(.+?)(?<!\\)`", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(ic)" + match.group(1) + "(ic)" + line[end:]
                for j in range(len(line_escape_pos)):
                    if line_escape_pos[j - 1] > end:
                        line_escape_pos[j - 1] += 6
                    if line_escape_pos[j - 1] > start:
                        line_escape_pos[j - 1] += 3
        
        # Link
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)\[(.+?)\](?<!\\)\((.+?)(?<!\\)\)", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(l)(name)" + match.group(1) + "(address)" + match.group(2) + "(l)" + line[end:]
                name_start, name_end = match.span(1)
                address_len = len(match.group(2))
                for j in range(len(line_escape_pos)):
                    if line_escape_pos[j - 1] > end:
                        line_escape_pos[j - 1] += 17
                    elif line_escape_pos[j - 1] > name_start:
                        line_escape_pos[j - 1] += 8
        
        line, line_escape_pos = escape_markdown(line, line_escape_pos)
        
        escape_positions.append(line_escape_pos)
        lines[i] = line
        i += 1
    markdown_text = "(newline)".join(lines)
    
    return markdown_text, escape_positions

def escape_parsed(line, line_escape_pos):
    # (b) - bold
    finished = False
    while finished == False:
        match = re.search(r"(\(b\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\b)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (i) - italic
    finished = False
    while finished == False:
        match = re.search(r"(\(i\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\i)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (ic) - inline code
    finished = False
    while finished == False:
        match = re.search(r"(\(ic\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\ic)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (h1) - Heading 1
    finished = False
    while finished == False:
        match = re.search(r"(\(h1\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\h1)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (h2) - Heading 2
    finished = False
    while finished == False:
        match = re.search(r"(\(h2\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\h2)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (h3) - Heading 3
    finished = False
    while finished == False:
        match = re.search(r"(\(h3\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\h3)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (h4) - Heading 4
    finished = False
    while finished == False:
        match = re.search(r"(\(h4\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\h4)" + line[end:]
            line_escape_pos.append(start + 1)
        
        # (h5) - Heading 5
    finished = False
    while finished == False:
        match = re.search(r"(\(h5\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\h5)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (h6) - Heading 6
    finished = False
    while finished == False:
        match = re.search(r"(\(h6\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\h6)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (bq) - Blockquote
    finished = False
    while finished == False:
        match = re.search(r"(\(bq\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\bq)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (ul) - Unordered List
    finished = False
    while finished == False:
        match = re.search(r"(\(ul\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\ul)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (ol) - Ordered List
    finished = False
    while finished == False:
        match = re.search(r"(\(ol\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\ol)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (checked) - Checked Box
    finished = False
    while finished == False:
        match = re.search(r"(\(checked\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\checked)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (unchecked) - Unchecked Box
    finished = False
    while finished == False:
        match = re.search(r"(\(unchecked\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\unchecked)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # Links
    # (l)
    finished = False
    while finished == False:
        match = re.search(r"(\(l\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\l)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (name)
    finished = False
    while finished == False:
        match = re.search(r"(\(name\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\name)" + line[end:]
            line_escape_pos.append(start + 1)
        
    # (address)
    finished = False
    while finished == False:
        match = re.search(r"(\(address\))", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(\\address)" + line[end:]
            line_escape_pos.append(start + 1)
    
    return line, line_escape_pos

def escape_markdown(line, line_escape_pos):
    line = line.replace('\\\\', '\u0000')
    
    # Astericks
    finished = False
    while not finished:
        match = re.search(r"\\\*", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "*" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Backtick
    finished = False
    while not finished:
        match = re.search(r"\\`", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "`" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Open Bracket
    finished = False
    while not finished:
        match = re.search(r"\\\[", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "[" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Closed Bracket
    finished = False
    while not finished:
        match = re.search(r"\\\]", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "]" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Open Parentheses
    finished = False
    while not finished:
        match = re.search(r"\\\(", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "(" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Closed Parentheses
    finished = False
    while not finished:
        match = re.search(r"\\\)", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + ")" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Hashtag
    finished = False
    while not finished:
        match = re.search(r"\\#", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "#" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Hyphen
    finished = False
    while not finished:
        match = re.search(r"\\-", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "-" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
    
    # Backslash
    finished = False
    while not finished:
        match = re.search(r"\u0000", line)
        if not match:
            finished = True
        else:
            start, end = match.span()
            line = line[:start] + "\\" + line[end:]
            for j in range(len(line_escape_pos)):
                if line_escape_pos[j - 1] > end:
                    line_escape_pos[j - 1] -= 1
                    
    return line, line_escape_pos