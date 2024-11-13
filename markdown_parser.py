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

markdown_rules = {
    "heading6": (r'^(?<!\\)###### (.+)$', r"(h6)\1"),
    "heading5": (r'^(?<!\\)##### (.+)$', r"(h5)\1"),
    "heading4": (r'^(?<!\\)#### (.+)$', r"(h4)\1"),
    "heading3": (r'^(?<!\\)### (.+)$', r"(h3)\1"),
    "heading2": (r'^(?<!\\)## (.+)$', r"(h2)\1"),
    "heading1": (r'^(?<!\\)# (.+)$', r"(h1)\1"),
    "bold": (r'(?<!\\)\*\*(?=[^\*])(.+?)(?<!\\)\*\*', r"(b)\1(b)"),
    "italic": (r'(?<!\\)\*(?=[^\*])(.+?)(?<!\\)\*', r"(i)\1(i)"),
    "inline_code": (r'(?<!\\)`(.+?)(?<!\\)`', r"(ic)\1(ic)"),
    "link": (r'(?<!\\)\[(.+?)\](?<!\\)\((.+?)(?<!\\)\)', r"(l)(name)\1(address)\2(l)"),
    "blockquote": (r'^(?<!\\)> (.+)$', r"(bq)\1"),
    "checked_box": (r'^(?<!\\) - \[ \] (.+)$', r"(checked)\1"),
    "unchecked_box": (r'^(?<!\\) - \[x\] (.+)$', r"(unchecked)\1"),
    "unordered_list": (r'^(?<!\\) - (.+)$', r"(ul)\1"),
    "ordered_list": (r'^\d+\. (.+)$', r"(ol)\1"),
    "newline": (r'\n', r"(newline)")
}

def parse_markdown(markdown_text):
    for rule_name, (pattern, replacement) in markdown_rules.items():
        markdown_text = re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
        print(f"Processed rule: {rule_name}")
    markdown_text = unescape_markdown(markdown_text)
    
    return markdown_text