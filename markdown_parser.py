import re

markdown_rules = {
    "heading6": (r"^###### (.+)$", "(h6)\\1"),
    "heading5": (r"^##### (.+)$", "(h5)\\1"),
    "heading4": (r"^#### (.+)$", "(h4)\\1"),
    "heading3": (r"^### (.+)$", "(h3)\\1"),
    "heading2": (r"^## (.+)$", "(h2)\\1"),
    "heading1": (r"^# (.+)$", "(h1)\\1"),
    "bold": (r"(?<!\\)\*\*(?=[^\*])(.+?)(?<!\\)\*\*", "(b)\\1(b)"),
    "italic": (r"(?<!\\)\*(.+?)(?<!\\)\*", "(i)\\1(i)"),
    "inline_code": (r"(?<!\\)\`(.+?)(?<!\\)\`", "(ic)\\1(ic)"),
    "unordered_list": (r"^\ - (.+)$", "(ul)\\1"),
    "blockquote": (r"^> (.+)$", "(bq)\\1"),
    "escaped_asterisk": (r"\\\*", "*"),
    "escaped_backtick": (r"\\`", "`"),
    # "escaped_backslash": (r"\\\\", '\\'),
    "newline": (r"\n", "(newline)")
}

def parse_markdown(markdown_text):
    for rule_name, (pattern, replacement) in markdown_rules.items():
        markdown_text = re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
    return markdown_text