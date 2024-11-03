import re

markdown_rules = {
    "heading6": (r"^###### (.+)$", "(h6)\\1"),
    "heading5": (r"^##### (.+)$", "(h5)\\1"),
    "heading4": (r"^#### (.+)$", "(h4)\\1"),
    "heading3": (r"^### (.+)$", "(h3)\\1"),
    "heading2": (r"^## (.+)$", "(h2)\\1"),
    "heading1": (r"^# (.+)$", "(h1)\\1"),
    "unordered_list": (r"^\ - (.+)$", "(ul)\\1(ul)"),
    "newline": (r"\n", "(newline)")
}

def parse_markdown(markdown_text):
    lines = markdown_text.splitlines()
    processed = []
    
    # Bold
    for line in lines:
        astericks = -1
        pair1 = 0
        pair2 = 0
        space = 0
        i = 0
        while i < len(line):
            if pair1 == 0 and line[i] == "*":
                if i < len(line) - 1 and line[i + 1] == "*":
                    if i < len(line) - 2 and line[i + 2] == "*":
                        pair1 = 0
                    else:
                        pair1 = 1
                        astericks = i
            elif pair1 == 1 and pair2 == 0:
                if space == 0 and line[i] != "*":
                    space = 1
                elif space == 1 and line[i] == "*":
                    if i < len(line) - 1 and line[i + 1] == "*":
                        line = line[:i] + "(b)" + line[i + 2:]
                        line = line[:astericks] + "(b)" + line[astericks + 2:]
                        pair1 = 0
                        pair2 = 0
                        space = 0
            i = i + 1
        processed.append(line)
        
    lines = processed
    processed = []
                    
    # Italic
    for line in lines:
        astericks = -1
        space = 0
        i = 0
        while i < len(line):
            if line[i] == "*" and space == 0:
                astericks = i
            elif line[i] != "*" and astericks >= 0 and space == 0:
                space = 1
            elif line[i] == "*" and space == 1:
                line = line[:i] + "(i)" + line[i + 1:]
                line = line[:astericks] + "(i)" + line[astericks + 1:]
                astericks = -1
                space = 0
            i = i + 1
        processed.append(line)

    lines = processed
    processed = []
    
    # Inline Code
    for line in lines:
        tick = -1
        space = 0
        i = 0
        while i < len(line):
            if line[i] == "`" and space == 0:
                tick = i
            elif line[i] != "`" and tick >= 0 and space == 0:
                space = 1
            elif line[i] == "`" and space == 1:
                line = line[:i] + "(ic)" + line[i + 1:]
                line = line[:tick] + "(ic)" + line[tick + 1:]
                tick = -1
                space = 0
            i = i + 1
        processed.append(line)
    
    markdown_text = "\n".join(processed)
    
    for rule_name, (pattern, replacement) in markdown_rules.items():
        markdown_text = re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
    return markdown_text