# Understanding the Parser

## Overview

The parsing process happens in two main stages:

1. **[Parsing](https://github.com/T9Air/MarkEd/blob/main/parser-explanation.md)** \([markdown_parser.py](https://github.com/T9Air/MarkEd/blob/main/markdown_parser.py)\) - Converts markdown syntax to an intermediate format
2. **[Converting](https://github.com/T9Air/MarkEd/blob/main/Docs/converter-explanation.md)** \([converter.py](https://github.com/T9Air/MarkEd/blob/main/converter.py)\) - Transforms the intermediate format to formatted text

## The Parsing Process

### Stage 1: Preparation

1. The text is split into lines

### Stage 2: Handle Parse Characters

> The parser needs to make sure that any characters that were inputed by the user that are the same as an output, (ex: "(b)" - which is the command to bold text), are edited so that they are not interpreted by the converter as commands.

1. Process each line to check for any parse characters (ex: "(b)", "(i)", etc.)
2. Add a backslash after the first parentheses in each match
3. Add the location of each backslash to a list

### Stage 3: Parse The Markdown Code

1. Each line is processed for:
    - **Line-starting elements**
        - Headers
        - Lists
        - Blockquotes
        - Check Boxes
        - Code Blocks
    - **Inline elements**
        - Bold text
        - Italic text
        - Inline Code
        - Links
2. Update the backslash positions from [Stage 2](#stage-2-handle-parse-characters) based on what markdown has been found

### Stage 4: Intermediate Format

Text is converted to an intermediate format using special tags:

- `(h1)` to `(h6)` for headers
- `(b)` for bold
- `(i)` for italic
- `(ic)` for inline code
- `(bc)` for code blocks
- `(ul)` for unordered lists
- `(ol)` for ordered lists
- `(l)`, `(name)`, `(address)` for links

### Stage 5: Handle Markdown Escape Characters

1. Process each line for markdown escape characters (a backslash)
2. Remove the backslashes
3. Update the backslash positions from [Stage 2](#stage-2-handle-parse-characters) based on how many escape characters have been found
