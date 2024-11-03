import re

markdown_rules = {
    "heading6": (r"^###### (.+)$", "(h6)\\1"),
    "heading5": (r"^##### (.+)$", "(h5)\\1"),
    "heading4": (r"^#### (.+)$", "(h4)\\1"),
    "heading3": (r"^### (.+)$", "(h3)\\1"),
    "heading2": (r"^## (.+)$", "(h2)\\1"),
    "heading1": (r"^# (.+)$", "(h1)\\1"),
    "inline_code": (r"\`(.+)\`", "(ic)\\1(ic)"),
    "unordered_list": (r"^\ - (.+)$", "(ul)\\1(ul)"),
    "newline": (r"\n", "(newline)")
}

def parse_markdown(markdown_text):
    # Italic
    lines = markdown_text.splitlines()
    processed = []
    
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

    markdown_text = "\n".join(processed)
    
    for rule_name, (pattern, replacement) in markdown_rules.items():
        markdown_text = re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
    return markdown_text