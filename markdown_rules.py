import re

search_rules = {
    "newline": (r"\n", "(newline)"),
    "heading1": (r"^# (.+)$", "(h1)\\1(h1)"),
    "heading2": (r"^## (.+)$", "(h2)\\1(h2)"),
    "heading3": (r"^### (.+)$", "(h3)\\1(h3)"),
    "heading4": (r"^#### (.+)$", "(h4)\\1(h4)"),
    "heading5": (r"^##### (.+)$", "(h5)\\1(h5)"),
    "heading6": (r"^###### (.+)$", "(h6)\\1(h6)")
}