# Markdown Editor with Tab Management

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Opening Files](#opening-files)
  - [Saving Files](#saving-files)
  - [Managing Tabs](#managing-tabs)
  - [Additional Features](#additional-features)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This is a versatile Markdown Editor with advanced tab management features. The application allows users to create, open, save, and manage multiple markdown files simultaneously. It includes features such as tab reordering, spell checking, and customizable user preferences to enhance the user experience.

## Features
- **Tab Management**: Open multiple files in separate tabs and switch between them with ease.
- **File Operations**: Open and save markdown files with individual paths for each tab.
- **Spell Checker**: Integrated spell checking to highlight and correct misspelled words.
- **User Preferences**: Customize the editor's appearance and behavior, including themes and font sizes.
- **Checkboxes**: Add and manage checkboxes in markdown files for to-do lists and task tracking.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/markdown-editor.git
   cd markdown-editor
   ```

2. **Install Dependencies**:
   Install the required Python libraries using `pip`:
   ```bash
   pip install tkinter pyspellchecker
   ```

## Usage
### Opening Files
To open a markdown file, click the `Open File` button and select a file from your file system. The file will be loaded into a new tab, and you can start editing immediately.

### Saving Files
To save your changes, click the `Save File` button. If it's the first time saving, you'll be prompted to choose a location and filename. Subsequent saves will overwrite the existing file.

### Managing Tabs
- **Creating a New Tab**: Click the `+ Create New File` button to open a new tab.
- **Switching Tabs**: Click on a tab to switch to it. The content of the tab will be loaded into the editor.
- **Reordering Tabs**: (Implementation Pending) Drag and drop tabs to reorder them.
- **Deleting Tabs**: Click the `❌` button on a tab to close it. The editor will automatically switch to another tab.

### Additional Features
- **Spell Checking**: Automatically highlights misspelled words and provides suggestions for corrections.
- **Checkboxes**: Create interactive checkboxes in your markdown files using `- [ ]` for unchecked and `- [x]` for checked items.
- **User Preferences**: Customize the editor through a settings menu to change themes, font sizes, and other preferences.

## Contributing
Contributions are welcome! If you have any suggestions for new features or improvements, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the AGPL-3.0 License. See the `LICENSE` file for details.


