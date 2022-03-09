#!/usr/bin/env python3

import argparse
from datetime import date
from pathlib import Path
from typing import NamedTuple

import emoji
import pyperclip
import yaml
from pathvalidate import sanitize_filename

today = date.today()

d1 = today.strftime("%Y%m%d")

c = "-"

config_dir_name = ".config"
config_filename = ".clip2file.yaml"
config_path = Path.home() / config_dir_name / config_filename


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

    url_txt = text.strip()

    count = -1
    while count != len(url_txt):
        count = len(url_txt)
        url_txt = url_txt.strip()
        url_txt = url_txt.replace("  ", " ")
        url_txt = url_txt.replace(" ", "-")
        url_txt = url_txt.replace("--", "-")
    return url_txt.lower().strip()


def clear_clip():
    """ """
    pyperclip.copy("")


def validate(string_path):
    """
    Validate a string path.
    Check for some common mistakes entering file paths on linux.
    """

    string_path_parts = Path(string_path).parts

    home_parts = Path.home().parts

    if string_path_parts[0] == "/" and not string_path_parts[0:3] == home_parts:
        return Path.home() / "/".join(string_path_parts[1:])
    elif (
        string_path_parts[0:2] == home_parts[1:]
    ):  # check for duplication of home path no '/'
        return Path.home() / "/".join(string_path_parts[2:])
    elif (
        string_path_parts[0:3] == home_parts
    ):  # check for duplication of home path with '/'
        return Path.home() / "/".join(string_path_parts[3:])
    else:
        return Path.home() / string_path


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


def read_dict(path):
    """
    Returns dictionary, read from yaml file found at 'path'.
    """
    with open(path, mode="r") as stream:
        try:
            parsed_config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return parsed_config


def config_check():
    """
    Validate the config file.
    """

    msg = f" \n No config file found at '{config_path}'.\n\n Open a terminal and paste the following.\n\ncat << EOF > {config_path}\nlookup:\n    documents: {Path.home()}/Documents\nEOF\n"

    if not config_path.is_file():
        print(msg)
        exit()
    else:
        return read_dict(config_path)


# --------------------------------------------------
def main() -> None:

    args = get_args()
    flag_arg = args.list
    raw_pos1_arg = args.positional1
    pos2_arg = args.positional2

    parsed_config = config_check()

    try:
        if flag_arg is True:
            print(
                f"""Options for first argument are: {list(parsed_config["lookup"].keys())}"""
            )
            exit()

        if raw_pos1_arg is None and flag_arg is False:
            raise ValueError("No valid arguments entered, try --help, or -h.")

        if pos2_arg is None and flag_arg is False:
            raise ValueError("No description entered!")

        if pos2_arg is not None:
            description = sanitize_filename(pos2_arg[0:71], platform="windows")

        pos1_arg = validate(raw_pos1_arg)

        if pos1_arg.name.lower() in parsed_config["lookup"]:
            save_location = Path(parsed_config["lookup"][pos1_arg.name.lower()])
        else:
            raise ValueError(
                f"""Not a valid first positional argument! try one of these: {list(parsed_config["lookup"].keys())}"""
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
