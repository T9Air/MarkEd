# Supported Markdown Syntax

This document outlines all the markdown syntax currently supported by MarkEd.

## Headers

Headers are created using `#` symbols:

1. `# Header 1` - Largest header
2. `## Header 2`
3. `### Header 3`
4. `#### Header 4`
5. `##### Header 5`
6. `###### Header 6` - Smallest header

## Text Formatting

- **Bold**: Wrap text with double asterisks
  - Example: `**bold text**`
- *Italic*: Wrap text with single asterisks
  - Example: `*italic text*`
- `Inline Code`: Wrap text with backticks
  - Example: `` `inline code` ``

## Lists

### Unordered Lists

Use a hyphen with a space for bullet points:

- Example item 1
- Example item 2

Markdown:

```markdown
- Example item 1
- Example item 2
```

### Ordered Lists

Use numbers followed by a period:

1. First item
2. Second item

Markdown:

```markdown
1. First item
2. Second item
```

## Task Lists

- [x] Checked box: `- [x] Checked box`
- [ ] Unchecked box: `- [ ] Unchecked box`

## Links

Create links using the `[text](url)` syntax:

- Example: `[MarkEd Repository](https://github.com/T9Air/MarkEd)`
- Result: [MarkEd Repository](https://github.com/T9Air/MarkEd)

## Code Blocks

Add code blocks by having 3 backticks on one line: ```, followed by another 3 on a different line

```markdown
Code
Block
```

## Escaping Characters

To display any markdown characters as plain text, use a backslash before it:

- `\*` for *
- `\#` for #
- `\[` for [
- `\]` for ]
- `\(` for (
- `\)` for )
- `\-` for -
- `\\` for \
- `` \` `` for `
