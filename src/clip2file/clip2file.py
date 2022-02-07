#!/usr/bin/env python3

import argparse
from datetime import date
from pathlib import Path

#  from typing import NamedTuple, TextIO
from typing import NamedTuple

import emoji
import pyperclip

today = date.today()

d1 = today.strftime("%Y%m%d")

c = "-"

lookup = {
    "pashmisc": "/home/live/Downloads/school/2021-2022/pashley-misc",
    "4mc": "/home/live/Downloads/school/2021-2022/4MC",
    "ockmisc": "/home/live/Downloads/school/2021-2022/Ocklynge-misc",
    "owls": "/home/live/Downloads/school/2021-2022/Pashley-Owls-Year-2",
    "txt": "/home/live/1e_textfiles",
}


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

    args = get_args()
    flag_arg = args.list
    pos1_arg = args.positional1
    pos2_arg = args.positional2

    try:
        if flag_arg is True:
            print(f"Options for first argument are: {list(lookup.keys())}")
            exit()

        if pos1_arg is None and flag_arg is False:
            raise ValueError("No valid arguments entered, try --help, or -h.")

        if pos2_arg is None and flag_arg is False:
            raise ValueError("No description entered!")

        if pos2_arg is not None:
            description = pos2_arg[0:71]

        if pos1_arg in lookup:
            save_location = Path(lookup.get(pos1_arg))
        else:
            raise ValueError(
                f"Not a valid first positional argument! try one of these: {list(lookup.keys())}"
            )

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
            raise ValueError("Looks like a file of that name already exists!")

        print("New file created, at....")
        print(f"{destination}")

    except ValueError as e:
        exit(str(e))


# --------------------------------------------------
if __name__ == "__main__":
    main()
