import re

import mistune

html_rules = {
    "heading6": (r"<h6>(.+)</h6>", "(h6)\\1"),
    "heading5": (r"<h5>(.+)</h5>", "(h5)\\1"),
    "heading4": (r"<h4>(.+)</h4>", "(h4)\\1"),
    "heading3": (r"<h3>(.+)</h3>", "(h3)\\1"),
    "heading2": (r"<h2>(.+)</h2>", "(h2)\\1"),
    "heading1": (r"<h1>(.+)</h1>", "(h1)\\1"),
    "bold": (r"<strong>(.+)</strong>", "(b)\\1(b)"),
    "italic": (r"<em>(.+)</em>", "(i)\\1(i)"),
    "paragraph": (r"(?s)<p>(.+)</p>", "\\1")
}

markdown_rules = {
    "inline_code": (r"\`(.+)\`", "(ic)\\1(ic)"),
    "unordered_list": (r"^\ - (.+)$", "(ul)\\1(ul)"),
    "newline": (r"\n", "(newline)") 
}

def parse_markdown(markdown_text):
    for rule_name, (pattern, replacement) in markdown_rules.items():
        markdown_text = re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
    markdown_text = mistune.html(markdown_text)
    for rule_name, (pattern, replacement) in html_rules.items():
        markdown_text = re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
    return markdown_text
