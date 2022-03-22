#!/usr/bin/env python3

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import NamedTuple

import pyperclip
import yaml
from pathvalidate import ValidationError, sanitize_filename, validate_filepath

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


def remove_unicode(s):
    """Remove from 's' any unicode characters, including emoji."""

    string_encode = s.encode("ascii", "ignore")

    return string_encode.decode()


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


def validate_path(string_path):
    """
    Validate a string path.
    Check for some common mistakes entering file paths on linux.
    """

    try:
        validate_filepath(string_path, platform="windows")
    except ValidationError as e:
        print("\n ATTENTION! Input error.")
        print(f"\n {e}\n", file=sys.stderr)
        sys.exit(1)

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


def read_config(path):
    """
    Returns dictionary, read from yaml config file found at 'path'.
    """
    with open(path, mode="r") as stream:
        try:
            parsed_config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return parsed_config


def config_check():
    """
    Validate the config file layout and content. Returns config.
    """

    if not config_path.is_file():  # not exists
        print("\n It looks like this is the first run.\n")
        print(f""" Creating a new config file at "{config_path}".\n""")
        config = empty_config()
        makedir(config_path.parent)
        dumpdict(config, config_path)
        return config
    else:
        check_config = read_config(config_path)
        if check_config is not None:  # not empty file
            if "lookup" not in check_config.keys():
                new_config = empty_config()
                print(
                    "\n Older config file layout detected, updating config to new layout."
                )
                new_config["lookup"].update(check_config)
                dumpdict(new_config, config_path)
                return new_config  # when updated
            return check_config  # when latest
        return empty_config()  # when empty


def define_save_location(raw_pos1_arg):
    """
    Validate pos1_arg argument then returns a <class 'pathlib.PosixPath'> object for the "save_location".
    """
    # in work below
    if raw_pos1_arg in parsed_config["lookup"].keys():  # key present?
        if not get_path(raw_pos1_arg).is_dir():
            config_error_01(raw_pos1_arg)
        return get_path(raw_pos1_arg)
    else:  # not key, a directory
        pos1_arg = validate_path(raw_pos1_arg)
        key_name = pos1_arg.name.lower()
        if key_name in parsed_config["lookup"].keys():
            if parsed_config["lookup"].get(key_name) == str(pos1_arg):
                if not get_path(key_name).is_dir():
                    config_error_01(key_name)
                return get_path(key_name)
            else:
                config_error_02(pos1_arg)
                return get_path(key_name)
        else:
            dir_check(pos1_arg)
            dumpdict(parsed_config, config_path)
            return get_path(key_name)


def get_path(key_name):
    """
    Returns a <class 'pathlib.PosixPath'> object of dict key "key_name" value.
    """
    return Path(parsed_config["lookup"].get(key_name))


def config_error_01(key_name):
    """
    Resolves config file error, when directory path is missing from file system.
    """
    print("\n ATTENTION! Config file error 01 detected.\n")
    dir_check(Path(parsed_config["lookup"].get(key_name)))


def config_error_02(key_name):
    """
    Resolves config error when file system directory names are duplicated at multiple paths.
    """
    print("\n ATTENTION! Config file error 02 detected.")
    print(
        f""" "{key_name.name.lower()}" matches "{parsed_config['lookup'].get(key_name.name.lower())}" not "{str(key_name)}"."""
    )
    answer = input(" Update config file? [yN]\n")
    if answer.lower().startswith("y"):
        print(f"""\n Using directory path "{str(key_name)}".""")
        parsed_config["lookup"].update(create_dict_entry(key_name))
        dir_check(key_name)
        dumpdict(parsed_config, config_path)
    else:
        print(
            f"""\n Using directory path "{parsed_config['lookup'].get(key_name.name.lower())}"."""
        )


def dir_check(path):
    """
    Check existence of directory 'path' a <class 'pathlib.PosixPath'> object,
    create it if it does not exist. Add to dict 'config:lookup' if it does exist.
    """

    msg1 = f"""\n Directory path "{path}" exists.\n"""
    msg2 = f""" You can use 'clip2file {path.name.lower()}' next time.\n"""

    if path.is_dir():
        print(msg1)
        print(msg2)
    else:
        if not parsed_config["defaults"]["force-creation-of-new-directories"]:
            answer = input(
                f'\n Directory path "{path}" does not exist, create it? " [yN]\n'
            )
            if not answer.lower().startswith("y"):
                sys.exit("\n Bye!\n")
        makedir(path)
        print(msg2)
    parsed_config["lookup"].update(create_dict_entry(path))


def dumpdict(dict_name, path):
    """
    dump dict to yaml config file
    """
    with open(path, mode="w", encoding="utf-8") as file:
        # add comment line in file
        file.write("# clip2file config file, autogenerated, do not edit.\n")
        file.write("\n")
        yaml.safe_dump(dict_name, file, sort_keys=True, indent=4)
        print(f""" Config file "{path}" updated!\n""")


def makedir(dir_path):
    """
    Make new directory only if name doesn't exit as a file or directory.
    """
    if dir_path.is_file():
        sys.exit(
            f"""Fatal error, wanting to create directory "{dir_path}"
            but this exists already as a file.\n
            Please delete file "{dir_path}" first or use a different name.
            """
        )
    print(f""" Directory path "{dir_path}" created!\n""")
    Path.mkdir(dir_path, parents=True, exist_ok=True)


def create_dict_entry(path):
    """
    Creates the dictionary key, value pair
    from 'path' a <class 'pathlib.PosixPath'> object.
    """

    key = path.name.lower()
    value = str(path.resolve())

    return {key: value}


def empty_config():
    """
    Create new empty dictionary for config file.
    """
    config = {}
    config["lookup"] = {}
    config["defaults"] = {"force-creation-of-new-directories": False}
    return config


parsed_config = config_check()


def main() -> None:

    args = get_args()
    flag_arg = args.list
    raw_pos1_arg = args.positional1
    pos2_arg = args.positional2

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

        f_ext = ".txt"
        filename = d1 + c + to_url_style(description) + f_ext  # build new filename
        save_location = define_save_location(raw_pos1_arg)
        destination = save_location / filename  # Define destination filename
        rawcontent = pyperclip.paste()

        if rawcontent == "":
            raise ValueError("Nothing in clipboard, to paste!")

        else:
            content = remove_unicode(rawcontent)  # strip unicode from rawcontent.

        if not Path.is_file(destination):  # Check filename doesn't already exist.
            with destination.open(mode="w", encoding="utf-8") as fib:
                fib.write(content)  # paste contents of clipboard
                clear_clip()
        else:
            raise ValueError(" Looks like a file of that name already exists!\n")

        print(" New file created, at....")
        print(f" {destination}\n")

    except ValueError as e:
        exit(str(e))


# --------------------------------------------------
if __name__ == "__main__":
    main()
