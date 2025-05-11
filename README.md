# Word Bubble

![Word Bubble Logo](icon/app_icon.png)

**Word Bubble** is a desktop application that helps you learn words and their meanings through floating bubbles on your screen. With a simple and engaging interface, it’s designed for language learning (e.g., English or Persian) and supports various bubble display modes, light/dark themes, and word list management.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](https://github.com/kayko/word-bubble/releases)

## Features

- **Floating Bubbles**: Display words and meanings as floating bubbles with fade-out animations.
- **Diverse Display Modes**:
  - **Fixed**: Display in fixed positions (e.g., top-left, center, bottom-right).
  - **Animated**: Move bubbles left-to-right, right-to-left, or top-to-bottom.
  - **Cascading**: Show bubbles sequentially in horizontal or vertical lines with consistent spacing.
  - **Random**: Display in random positions on the screen.
- **Bilingual Support**: Interface in Persian and English.
- **Light and Dark Themes**: Switch between light and dark themes for the UI and window title bars.
- **Word List Management**: Add, edit, delete, and select word lists.
- **Advanced Settings**:
  - Adjust bubble display duration and interval between bubbles.
  - Choose bubble positions, font size, colors (word, meaning, background), and opacity.
  - Select fonts (supports custom fonts like Vazir).
- **Word Playback Modes**: Sequential or random playback of words from the selected list.
- **Always on Top**: Option to keep bubbles above other windows.

## Prerequisites

To run **Word Bubble**, you need:

- **Operating System**: Windows 10 or 11 (Linux and macOS support not tested).
- **Python**: Version 3.7 or higher.
- **Libraries**:
  - PyQt5 (`pip install PyQt5`)
- **Fonts**: Vazir font (included in `fonts/`) or any compatible font.
- **Icon Assets**: PNG images for buttons (included in `icon/`).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kayko/word-bubble.git
   cd word-bubble
   ```

2. **Install Dependencies**:
   Install the PyQt5 library:
   ```bash
   pip install PyQt5
   ```

3. **Verify Required Files**:
   Ensure the following folders exist in the project directory:
   - `fonts/`: Contains `Vazir.ttf` (for Persian text support).
   - `icon/`: Contains PNG files like `settings.png`, `pause.png`, `play.png`, `list.png`, `app_icon.png`.

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

1. **Initial Setup**:
   - Run the program with `python main.py`.
   - The main window opens, featuring the following buttons:
     - **Play/Pause**: Start or pause bubble display.
     - **Settings**: Configure bubble display options.
     - **Manage Words and Lists**: Add/edit word lists and words.
     - **Play Mode**: Choose sequential or random playback.
     - **Select List**: Pick a word list for display.
     - **Dark Mode**: Toggle between dark and light themes.

2. **Adding Words**:
   - Click the “Manage Words and Lists” button.
   - Create a new list or select an existing one.
   - Add words and meanings in the format `word,meaning` (e.g., `Hello,سلام`).

3. **Configuring Display**:
   - In the settings window, you can:
     - **Bubble Position**: Select fixed, animated, cascading, or random modes.
     - **Display Duration**: Set how long each bubble stays (e.g., 5–20 seconds).
     - **Interval**: Set the time between bubbles (e.g., 10–30 seconds).
     - **Colors**: Choose colors for words, meanings, and bubble backgrounds.
     - **Font and Size**: Select a font (e.g., Vazir) and text size.
     - **Opacity**: Adjust bubble transparency.
     - **Always on Top**: Enable bubbles to stay above other windows.

4. **Choosing Play Mode**:
   - In the “Play Mode” window, select “Sequential” (words in order) or “Random” (words randomly).

5. **Starting Display**:
   - Select a word list (via the “Select List” button).
   - Click “Play” to display bubbles with the chosen settings.

## Project Structure

- **`main.py`**: Entry point, initializes the application and main window.
- **`app.py`**: Core application logic, manages the UI and bubble control.
- **`bubble.py`**: `Bubble` class for creating and displaying floating bubbles.
- **`settings_dialog.py`**: Settings window for configuring bubble display.
- **`word_list_manager.py`**: Manages word lists and word addition/editing.
- **`custom_input_dialog.py`**: Custom input dialogs for list selection and play mode.
- **`utils.py`**: Utility functions like title bar theme setting and RTL text detection.
- **`fonts/`**: Contains custom fonts (e.g., `Vazir.ttf`).
- **`icon/`**: Contains PNG images for buttons and app icon.

## Version

- **Current Version**: 1.0.0
- **Release Date**: May 11, 2025
- **Recent Changes**:
  - Fixed irregular bubble spacing in cascading modes.
  - Corrected title bar theme in dark mode for “Play Mode” and “Select List” windows.
  - Increased width of “Play Mode” and “Select List” windows for full title display.

## Known Issues

- **Cascading Modes**: In high-resolution displays or specific settings, bubble spacing may require manual adjustment.
- **OS Support**: Tested on Windows; Linux and macOS may require additional configuration.
- **Fonts**: If Vazir font is unavailable, the app falls back to Arial, which may not be optimal for Persian text.

## Development and Contribution

We welcome contributions to improve **Word Bubble**! To contribute:

1. Fork the repository:
   ```bash
   git clone https://github.com/kayko/word-bubble.git
   ```
2. Make your changes and submit a Pull Request.
3. Report issues or suggestions in the [Issues](https://github.com/kayko/word-bubble/issues) section.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Developer

- **Kayko**

## Acknowledgments

Thank you for using **Word Bubble**! We hope this tool enhances your language learning experience.

---

*Last Updated: May 11, 2025*