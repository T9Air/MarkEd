import re

def unescape_markdown(text):
    text = text.replace('\\\\', '\u0000')
    
    replacements = [
        ('\\*', '*'),
        ('\\_', '_'),
        ('\\`', '`'),
        ('\\[', '['),
        ('\\]', ']'),
        ('\\(', '('),
        ('\\)', ')'),
        ('\\#', '#'),
        ('\\-', '-'),
    ]
    
    for escaped, unescaped in replacements:
        text = text.replace(escaped, unescaped)
    
    text = text.replace('\u0000', '\\')
    
    return text

def parse_markdown(markdown_text):
    lines = markdown_text.splitlines()
    escape_positions = []    
    i = 0
    
    for line in lines:
        line_escape_pos = []
        finished = False
        while finished == False:
            match = re.search(r"(\(b\))", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(\\b)" + line[end:]
                line_escape_pos.append(start + 1)
        escape_positions.append(line_escape_pos)
##########################################################################
        # Markdown code for the beggining of the line
        if line.startswith("###### "): # Heading 6
            line = "(h6)" + line[7:]
            for j in line_escape_pos:
                line_escape_pos[j] -= 3
        elif line.startswith("##### "): # Heading 5
            line = "(h5)" + line[6:]
            for j in line_escape_pos:
                line_escape_pos[j] -= 2
        elif line.startswith("#### "): # Heading 4
            line = "(h4)" + line[5:]
            for j in line_escape_pos:
                line_escape_pos[j] -= 1
        elif line.startswith("### "): # Heading 3
            line = "(h3)" + line[4:]
        elif line.startswith("## "): # Heading 2
            line = "(h2)" + line[3:]
            for j in line_escape_pos:
                line_escape_pos[j] += 1
        elif line.startswith("# "): # Heading 1
            line = "(h1)" + line[2:]
            for j in line_escape_pos:
                line_escape_pos[j] += 2
        elif line.startswith("> "): # Blockquote
            line = "(bq)" + line[2:]
        elif line.startswith(" - [x] "): # Checked Box
            line = "(checked)" + line[7:]
        elif line.startswith(" - [ ] "): # Unchecked Box
            line = "(unchecked)" + line[7:]
        elif line.startswith(" - "): # Unordered List
            line = "(ul)" + line[3:]
        elif re.match(r"^\d+\. ", line): # Ordered List
            match = re.match(r"^\d+\. ", line)
            line = "(ol)" + line[match.end():]
        
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
        
        # Italic
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)\*(?=[^\*])(.+?)(?<!\\)\*", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(i)" + match.group(1) + "(i)" + line[end:]
        
        # Inline Code
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)`(.+?)(?<!\\)`", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(ic)" + match.group(1) + "(ic)" + line[end:]
        
        # Link
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)\[(.+?)\](?<!\\)\((.+?)(?<!\\)\)", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(l)(name)" + match.group(1) + "(address)" + match.group(2) + "(l)" + line[end:]
        
        lines[i] = line
        i += 1
    markdown_text = "(newline)".join(lines)
    
    markdown_text = unescape_markdown(markdown_text)
    
    return markdown_text, escape_positions