import re

search_rules = {
    #"heading1": (r"^# (.+)$", "(h1)\\1(h1)"),
    #"heading2": (r"^## (.+)$", "(h2)\\1(h2)"),
    #"heading3": (r"^### (.+)$", "(h3)\\1(h3)"),
    #"heading4": (r"^#### (.+)$", "(h4)\\1(h4)"),
    #"heading5": (r"^##### (.+)$", "(h5)\\1(h5)"),
    #"heading6": (r"^###### (.+)$", "(h6)\\1(h6)"),
    #"italic": (r"\*(.+)\*", "(i)\\1(i)"),
    #"bold": (r"\*\*(.+)\*\*", "(b)\\1(b)"),
    #"blockquote": (r"^> (.+)$", "(bq)\\1(bq)"),
    #"orderedlist": (r"^\d+\. (.+)$", "(ol)\\1(ol)"),
    #"unorderedlist": (r"^\ - (.+)$", "(ul)\\1(ul)"),
    #"link": (r"\[(.+)]\((.+)\)"),
    #"image": (r"!\[(.+)]\((.+)\)"),
    "newline": (r"\n", "(newline)")
}