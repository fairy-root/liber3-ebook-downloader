# Liber3 ebook downloader

**Liber3 ebook downloader** is a reverse engineered API and a Python-based tool that searches for ebooks on **[Liber3](https://liber3.eth.limo/)**, filters the results based on language and file format, and downloads the selected ebooks. The tool uses a configuration file (`config.json`) to persist user preferences. If no config file is found, the user is prompted to set their filters. The user may specify `"all"` for either filter to disable filtering for that category.

## Features

- **Configurable Filters:** 
    - Specify a preferred language and file format (or use `"all"` to disable filtering).
    - User preferences are saved in `config.json` for subsequent runs.
- **Colored Terminal Output:** 
    - Uses color-coded messages to enhance user feedback.
- **Ebook Downloading:** 
    - Searches and lists matching ebooks.
    - Allows selecting one or multiple entries for download.
    - Downloads files into organized directories based on the author's name.

## Requirements

- **Python:** 3.6 or later  
- **Python Libraries:** 
    - **[requests](https://pypi.org/project/requests/)**
- **Other:** 
    - Internet connectivity

---

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/fairy-root/liber3-ebook-downloader.git
    cd liber3-ebook-downloader
    ```
2. **Install Dependencies**:
    ```bash
    pip install requests
    ```

## Usage

1. **Run the Script**:
    ```bash
    python main.py
    ```

2. **Behavior**:

    - No config.json: The script prompts for preferred language and file format.

    - Existing config.json: Loads preferences silently.

    - Search: Enter a book name to search.

    - Select & Download: Choose one or multiple entries (or "all") from the list of filtered results. The tool then downloads the selected ebooks into the appropriate folder.

## Basic Expected Output

- **Initial Prompt**:
    The script asks for a book or author name.

- **Search Results**:
    A numbered list of ebooks is displayed with details such as title, author, language, file format, and size.

- **Download Process**:
    After inputting your selection, the script shows download progress messages and confirms when a download is successful. Files are saved under a directory structure like Downloads/<Author>/.

---

## Critique & Future Improvements

- **Modularity**:
    The code can be refactored into separate modules for configuration, search, and download to enhance maintainability.

- **Error Handling & Logging**:
    Adding a robust logging system to complement the colored output for better debugging and production use.

- **Extensibility**:
    Future features could include additional filters, a graphical user interface, or support for multiple ebook sources.

---

## Donation

Your support is appreciated:

- **USDt (TRC20)**: `TGCVbSSJbwL5nyXqMuKY839LJ5q5ygn2uS`
- **BTC**: `13GS1ixn2uQAmFQkte6qA5p1MQtMXre6MT`
- **ETH (ERC20)**: `0xdbc7a7dafbb333773a5866ccf7a74da15ee654cc`
- **LTC**: `Ldb6SDxUMEdYQQfRhSA3zi4dCUtfUdsPou`

## Author and Contact

- **GitHub**: [FairyRoot](https://github.com/fairy-root)
- **Telegram**: [@FairyRoot](https://t.me/FairyRoot)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.
