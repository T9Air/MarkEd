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
        # Escape any characters that would be a parsed output
        line_escape_pos = []
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
                          
        # Parse Markdown
        # Markdown code for the beggining of the line
        if line.startswith("###### "): # Heading 6
            line = "(h6)" + line[7:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 7
        elif line.startswith("##### "): # Heading 5
            line = "(h5)" + line[6:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 6
        elif line.startswith("#### "): # Heading 4
            line = "(h4)" + line[5:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 5
        elif line.startswith("### "): # Heading 3
            line = "(h3)" + line[4:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 4
        elif line.startswith("## "): # Heading 2
            line = "(h2)" + line[3:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 3
        elif line.startswith("# "): # Heading 1
            line = "(h1)" + line[2:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 2
        elif line.startswith("> "): # Blockquote
            line = "(bq)" + line[2:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 2
        elif line.startswith(" - [x] "): # Checked Box
            line = "(checked)" + line[7:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 7
        elif line.startswith(" - [ ] "): # Unchecked Box
            line = "(unchecked)" + line[7:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 7
        elif line.startswith(" - "): # Unordered List
            line = "(ul)" + line[3:]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= 3
        elif re.match(r"^\d+\. ", line): # Ordered List
            match = re.match(r"^\d+\. ", line)
            line = "(ol)" + line[match.end():]
            for j in range(len(line_escape_pos)):
                line_escape_pos[j - 1] -= match.end()
        
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
                        line_escape_pos[j - 1] -= 2
                    if line_escape_pos[j - 1] > start:
                        line_escape_pos[j - 1] -= 2
                    
        
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
                        line_escape_pos[j - 1] -= 1
                    if line_escape_pos[j - 1] > start:
                        line_escape_pos[j - 1] -= 1
        
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
                        line_escape_pos[j - 1] -= 1
                    if line_escape_pos[j - 1] > start:
                        line_escape_pos[j - 1] -= 1
        
        # Link
        finished = False
        while not finished:
            match = re.search(r"(?<!\\)\[(.+?)\](?<!\\)\((.+?)(?<!\\)\)", line)
            if not match:
                finished = True
            else:
                start, end = match.span()
                line = line[:start] + "(l)(name)" + match.group(1) + "(address)" + match.group(2) + "(l)" + line[end:]
        
        escape_positions.append(line_escape_pos)
        lines[i] = line
        i += 1
    markdown_text = "(newline)".join(lines)
    
    markdown_text = unescape_markdown(markdown_text)
    
    return markdown_text, escape_positions