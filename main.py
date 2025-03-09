from requests import Response, Session, exceptions
from urllib.parse import quote
from typing import Dict
import json
import os
import re

CONFIG_FILE = "config.json"
s = Session()

def print_colored(text: str, color: str) -> None:
    colors: Dict[str, str] = {
        "green": "\033[92m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "orange": "\033[38;5;208m",
        "purple": "\033[38;5;129m",
        "teal": "\033[38;5;6m",
        "lime": "\033[38;5;10m",
    }
    color_code: str = colors.get(color.lower(), "\033[0m")
    colored_text: str = f"{color_code}{text}\033[0m"
    print(colored_text)

def input_colored(prompt: str, color: str) -> str:
    colors: Dict[str, str] = {
        "green": "\033[92m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "orange": "\033[38;5;208m",
        "purple": "\033[38;5;129m",
        "teal": "\033[38;5;6m",
        "lime": "\033[38;5;10m",
    }
    color_code: str = colors.get(color.lower(), "\033[0m")
    colored_prompt: str = f"{color_code}{prompt}\033[0m"
    return input(colored_prompt)

def sanitize_filename(filename: str) -> str:
    """
    Replace forbidden characters in a filename with underscores.
    """
    return re.sub(r'[\\/*?:"<>|]', "_", filename)
    
def load_config():
    """Load the language and extension filter from config.json if available."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                if "language" in config and "extension" in config:
                    return config
        except (json.JSONDecodeError, IOError):
            print_colored("Error reading config.json. Recreating file...", "red")
    return None

def save_config(language, extension):
    """Save user-selected language and extension filters to config.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"language": language, "extension": extension}, f, indent=4)

def get_user_filters():
    """Prompt the user to enter language and extension filters."""
    print_colored("No config found. Please set your filters.", "yellow")
    language = input_colored("Enter preferred language (e.g., English or 'all' for any): ", "cyan").strip()
    extension = input_colored("Enter preferred file format (e.g., pdf, epub, mobi or 'all' for any): ", "cyan").strip()
    
    save_config(language, extension)
    return {"language": language, "extension": extension}

def search_books(query: str) -> list[dict[str, str]]:
    url = "https://lgate.glitternode.ru/v1/searchV2"
    headers = {
        "Host": "lgate.glitternode.ru",
        "Content-Length": "41",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua": '"Chromium";v="133", "Not(A:Brand";v="99"',
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Origin": "https://liber3.eth.limo",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Storage-Access": "active",
        "Referer": "https://liber3.eth.limo/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
    }
    data: dict[str, str] = {"address": "", "word": query}
    try:
        response: Response = s.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print_colored(
                f"Error: Search request failed with status {response.status_code}",
                "red",
            )
            return []
        books = response.json()["data"]["book"]
        config = load_config()
        if not config:
            config = get_user_filters()

        language_filter = config["language"].lower()
        extension_filter = config["extension"].lower()

        # Apply filters: if the user selected "all", then don't filter on that field.
        filtered_books = [
            book for book in books 
            if (language_filter == "all" or book["language"].lower() == language_filter) and
               (extension_filter == "all" or book["extension"].lower() == extension_filter)
        ]
        return filtered_books
            
    except exceptions.RequestException as e:
        print_colored(f"Error during request: {e}", "red")
        return []
    except KeyError as e:
        print_colored(f"Error in response format: {e}", "red")
        return []
    except IOError as e:
        print_colored(f"File I/O error: {e}", "red")
        return []
    except Exception as e:
        print_colored(f"Error during download: {e}", "red")
        return []

def download(cid: str, title: str, extension: str, author: str) -> bool:
    title_urlencoded = quote(title)
    author_urlencoded = quote(author)
    url = f"https://gateway-ipfs.st/ipfs/{cid}?filename={title_urlencoded}_{author_urlencoded}_liber3.{extension}"
    headers: dict[str, str] = {
        "Host": "gateway-ipfs.st",
        "Sec-Ch-Ua": '"Chromium";v="133", "Not(A:Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Accept-Language": "en-US,en;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://liber3.eth.limo/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
    }
    try:
        response: Response = s.get(url, headers=headers)
        if response.status_code != 200:
            print_colored(
                f"Error: Download failed with status {response.status_code}", "red"
            )
            return False
        content = response.content
        safe_author = sanitize_filename(author)
        author_folder = os.path.join("Downloads", safe_author)
        os.makedirs(author_folder, exist_ok=True)
        safe_filename = sanitize_filename(f"{title}_{author}.{extension}")
        full_path = os.path.join(author_folder, safe_filename)
        with open(full_path, "wb") as f:
            f.write(content)
        return True
    except exceptions.RequestException as e:
        print_colored(f"Error during request: {e}", "red")
        return False
    except KeyError as e:
        print_colored(f"Error in response format: {e}", "red")
        return False
    except IOError as e:
        print_colored(f"File I/O error: {e}", "red")
        return False
    except Exception as e:
        print_colored(f"Error during download: {e}", "red")
        return False

def main():
    try:
        query: str = input_colored("Enter a book or author name: ", "cyan")
        print_colored("Searching for books...", "blue")
        books: list[dict[str, str]] = search_books(query)

        if not books:
            print_colored("No books found matching your query", "yellow")
            return

        print_colored("\nSearch Results:", "green")
        # Colors for rotating through book listings
        colors = [
            "cyan",
            "magenta",
            "yellow",
            "green",
            "blue",
            "purple",
            "teal",
            "orange",
            "lime",
        ]

        for index, book in enumerate(books):
            title: str = book["title"]
            author: str = book["author"]
            extension: str = book["extension"]
            language: str = book["language"]
            filesize: str = book["filesize"]
            size: float = int(filesize) / 1024 / 1024
            color = colors[index % len(colors)]
            book_info = f"{index + 1}. {title} - {author} ({language}, {extension}, {size:.2f} MB)"
            print_colored(book_info, color)

        # Prompt for one or more choices or 'all'
        choice_input: str = input_colored(
            "\nEnter your choice(s) (e.g. '1' or '1,2,3' or 'all'): ", "cyan"
        ).strip()

        choices_to_download = []
        if choice_input.lower() == "all":
            choices_to_download = list(range(1, len(books) + 1))
        else:
            try:
                # Split the input on commas and remove extra whitespace.
                choices_str_list = choice_input.split(",")
                choices_to_download = [int(item.strip()) for item in choices_str_list if item.strip()]
            except ValueError:
                print_colored("Invalid input. Please enter valid numbers separated by commas or 'all'.", "red")
                return

            # Validate choices are within valid range.
            for choice in choices_to_download:
                if choice < 1 or choice > len(books):
                    print_colored(
                        f"Invalid choice {choice}. Please select numbers between 1 and {len(books)}.",
                        "red",
                    )
                    return

        # Remove duplicates and sort the choices.
        choices_to_download = sorted(set(choices_to_download))

        # Process each selected book.
        for choice in choices_to_download:
            book = books[choice - 1]
            title: str = book["title"]
            author: str = book["author"]
            extension: str = book["extension"]
            cid = book["ipfs_cid"]

            print_colored(f"Downloading {title} by {author}...", "blue")
            success = download(cid, title, extension, author)
            if success:
                print_colored(f"Downloaded {title} - {author}.{extension}", "green")
            else:
                print_colored(f"Failed to download {title} - {author}.{extension}", "red")

    except KeyboardInterrupt:
        print_colored("\nOperation canceled by user", "yellow")
    except Exception as e:
        print_colored(f"An unexpected error occurred: {e}", "red")

if __name__ == "__main__":
    main()