
# clip2file

clip2file is a Python command line application, which will write text from the clipboard to a new file.


## Features

- Writes text from the primary clipboard to a new text file
- Creates the directory path to the new file (if required).
- Creates a directory lookup name, which can be used to save typing the full directory path on successive runs.
- Automatically creates/updates a config file as required.
- Automatically sanitizes the new files filename.
- Automatically prepends date to new files filename.
- Removes any emoji from the clipboard text prior to writing to the file.

## Demo

![Example](./readme_resources/termtosvg_bzl9wjja.svg)

![Example](./readme_resources/termtosvg_nvnljepz.svg)


## Support

Only tested on Linux OS running Python 3.7.2

On Linux, this application makes use of the xsel command, which should come with the os. Otherwise run "sudo apt-get install xsel" or search your distrubutions package repository.


## Installation

Using the linux command line. Install clip2file from github into a Python virtual environment.

```bash
  cd ~
  python3 -m venv .venv        # create virtual environment
  source .venv/bin/activate    # activate environment
  python3 -m pip install git+https://github.com/mpflynnx/clip2file.git     # install from git

```
    
## Usage/Examples

Copy text to the clipboard from any available source, i.e. webpage, pdf or document.

On the Linux command line enter:

```bash
clip2file <lookup name or directory path to store the new file> "text describing the contents of file"

# using the path to directory 'notes' in /home/username.
# thereafter lookup name 'notes' can be used instead of the long directory path.
clip2file a/directory/deep/in/my/home/for/notes "some notes on subject xyz"

# Using lookup name 'notes'
clip2file notes "some more notes on subject xyz"
```


## Roadmap

- Microsoft Windows support.
- Auto preview of new file contents.
- Append to existing file if filenames match.
- Auto wrap text in file.
- Allow a change of default extension from .txt
- Tests


## Badges

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)


