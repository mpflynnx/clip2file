#!/usr/bin/env python3

import argparse
from datetime import date
from pathlib import Path
from typing import NamedTuple, TextIO

import emoji
import pyperclip

today = date.today()

d1 = today.strftime("%Y%m%d")

c = "-"


class Args(NamedTuple):
    """Command-line arguments"""

    positional1: str
    positional2: str
    list: bool


def to_url_style(text):
    """
    Process text string.
    """
    if not text:
        return text

    text = text.strip()
    url_txt = ""
    for ch in text:
        url_txt += ch if ch.isalnum() or ch == "." else " "

    count = -1
    while count != len(url_txt):
        count = len(url_txt)
        url_txt = url_txt.strip()
        url_txt = url_txt.replace("  ", " ")
        url_txt = url_txt.replace(" ", "-")
        url_txt = url_txt.replace("--", "-")
        url_txt = url_txt.replace(".", "-")  # mf added to replace '.' with '-'
    return url_txt.lower().strip()


def clear_clip():
    """ """
    pyperclip.copy("")


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Creates a new file that contains the contents of the clipboard.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "positional1",
        metavar="str",
        nargs="?",
        help="Enter a option, see --list or -l for details.",
    )

    parser.add_argument(
        "positional2",
        metavar="str",
        nargs="?",
        help="Enter a description of the new files contents in double quotes.",
    )

    parser.add_argument(
        "-l",
        "--list",
        help="List available options for first positional argument.",
        action="store_true",
    )

    args = parser.parse_args()

    return Args(args.positional1, args.positional2, args.list)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    flag_arg = args.list
    pos1_arg = args.positional1
    pos2_arg = args.positional2

    try:
        if flag_arg == True:
            print("Options for pos1_arg = 'pashmisc', '4mc', 'ockmisc', 'owls', 'txt'")
            exit()

        if pos1_arg == "pashmisc":
            save_location = Path("/home/live/Downloads/school/2021-2022/pashley-misc")

        elif pos1_arg == "4mc":
            save_location = Path("/home/live/Downloads/school/2021-2022/4MC")

        elif pos1_arg == "ockmisc":
            save_location = Path("/home/live/Downloads/school/2021-2022/Ocklynge-misc")

        elif pos1_arg == "owls":
            save_location = Path(
                "/home/live/Downloads/school/2021-2022/Pashley-Stephen-Owls-Year-2"
            )

        elif pos1_arg == "txt":
            save_location = Path("/home/live/1e_textfiles")

        elif pos1_arg == None and flag_arg == False:
            raise ValueError("No valid arguments entered, try --help, or -h.")

        if pos2_arg == None and flag_arg == False:
            raise ValueError("No description entered.")
        elif not pos2_arg == None:
            description = pos2_arg[0:71]

        f_ext = ".txt"
        filename = d1 + c + to_url_style(description) + f_ext  # build new filename
        destination = save_location / filename  # Define destination filename
        rawcontent = pyperclip.paste()

        if rawcontent == "":
            raise ValueError("Nothing in clipboard, to paste!")

        else:
            content = emoji.get_emoji_regexp().sub(
                "", rawcontent
            )  # strip emoji from rawcontent.

        if not Path.is_file(destination):  # Check filename doesn't already exist.
            with destination.open(mode="w", encoding="utf-8") as fib:
                fib.write(content)  # paste contents of clipboard
                clear_clip()
        else:
            # clear_clip()  # clear content of clipboard.
            raise ValueError("Looks like a file of that name already exists!")

        print("New file created, at....")
        print(f"{destination}")

    except ValueError as e:
        exit(str(e))


# --------------------------------------------------
if __name__ == "__main__":
    main()
