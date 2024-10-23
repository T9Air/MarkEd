import re

search_rules = {
    "heading6": (r"^###### (.+)$", "(h6)\\1"),
    "heading5": (r"^##### (.+)$", "(h5)\\1"),
    "heading4": (r"^#### (.+)$", "(h4)\\1"),
    "heading3": (r"^### (.+)$", "(h3)\\1"),
    "heading2": (r"^## (.+)$", "(h2)\\1"),
    "heading1": (r"^# (.+)$", "(h1)\\1"),
    "bold&italic": (r"\*\*\*(.+)\*\*\*", "(bi)\\1(bi)"),
    "bold": (r"\*\*(.+)\*\*", "(b)\\1(b)"),
    "italic": (r"\*(.+)\*", "(i)\\1(i)"),
    "blockquote": (r"^> (.+)$", "(bq)\\1(bq)"),
    "orderedlist": (r"^\d+\. (.+)$", "(ol)\\1(ol)"),
    "unorderedlist": (r"^\ - (.+)$", "(ul)\\1(ul)"),
    "link": (r"\[(.+)]\((.+)\)", "(link)(text)\\1(text)(address)\\2(address)(link)"),
    "image": (r"!\[(.+)]\((.+)\)", "(image)(text)\\1(text)(address)\\2(address)(image)"),
    "newline": (r"\n", "(newline)")    
}

def parse_markdown(markdown_text):
    for rule_name, (pattern, replacement) in search_rules.items():
        markdown_text = re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
    print(markdown_text)
    return markdown_text