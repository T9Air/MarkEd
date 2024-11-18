# Understanding the Converter

This document explains how the converter transforms the parsed markdown into formatted text.

## Overview

The parsing process happens in two main stages:

1. **[Parsing](https://github.com/T9Air/MarkEd/blob/main/parser-explanation.md)** \([markdown_parser.py](https://github.com/T9Air/MarkEd/blob/main/markdown_parser.py)\) - Converts markdown syntax to an intermediate format
2. **[Converting](https://github.com/T9Air/MarkEd/blob/main/Docs/converter-explanation.md)** \([converter.py](https://github.com/T9Air/MarkEd/blob/main/converter.py)\) - Transforms the intermediate format to formatted text

## The Conversion Process

### Stage 1: Text Processing

1. **Line Processing**
   - Splits text at `(newline)` markers
   - Processes each line separately
   - Maintains ordered list numbering

### Stage 2: Style Application

1. **Basic Formatting**
   - Font sizes for headers
   - Bold and italic text
   - Background colors for code blocks
   - Link colors and underlining

2. **Special Elements**
   - Bullet points for unordered lists
   - Numbers for ordered lists
   - Checkbox symbols
   - Blockquote backgrounds

### Stage 3: Tag Management

The converter creates Tkinter tags that combine:

- Font properties (size, weight, style)
- Text colors
- Background colors
- Text decorations (underline)

## Implementation Details

- Uses Tkinter's tag system for formatting
- Maintains character positions for proper formatting
- Processes escape sequences
