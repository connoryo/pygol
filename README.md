# pygol

A simple CLI simulator for Conway's Game of Life written in Python.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Commands and Options](#commands-and-options)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Description

pygol (**PY**thon **G**ame **O**f **L**ife) is a simple CLI python app that implements [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). This project was inspired by Robert Heaton's [Game of Life tutorial](https://robertheaton.com/2018/07/20/project-2-game-of-life/).

The program includes a number of starting boards to choose from, as well as support for custom user-defined boards. pygol is aimed to give users a fun command line screensaver with minimal setup effort.

## Installation

- Download the `pygol-[version].whl` file from the [latest release](https://github.com/connoryo/pygol/releases/latest) into your Python project.
- Create a new virtual environment, or activate an existing one.

```bash
python3 -m venv env
source env/bin/activate
```

- Install the wheel.

```bash
pip install pygol-[version]-none-any.whl
```

### Requirements

- Python 3.8+
- Unix-based system (macOS or Linux)

### From Source

- Clone the repo to your desired directory

```bash
git clone git@github.com:connoryo/pygol.git
```

- (Recommended) Set up a virtual environment

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
```

- Install the library and its dependencies with `poetry`

```bash
$ pip install poetry
...
Successfully installed poetry-1.8.3
$ poetry install
Installing dependencies from lock file
...
Installing the current project: pygol (0.0.1)
```

- Verify installation with `pytest`

```bash
$ pwd
.../pygol # root directory of the repo
$ pytest
...
================ 8 passed in 0.04s ================
```

## Usage

After installation, the program can be run without any arguments for a simple 'beacon' example.

```bash
$ pygol
┌──────────┐
│          │
│          │
│  ██████  │
│          │
│          │
└──────────┘
┌──────────┐
│          │
│    ██    │
│    ██    │
│    ██    │
│          │
└──────────┘
...
```

## Commands and Options

- `-h | --help`: Show help message and exit.
- `-b | --board {beacon,gospel_glider_gun,toad,glider,blinker,custom,random}`: The starting board to simulate. If set to custom, you must specify an input file. Default is 'beacon'.
- `-i | --input INPUT`: A txt file of 1s and 0s arranged in rows representing a starting board when using the 'custom' board. See the `boards` directory for examples.
- `-a | --alive-proportion ALIVE_PROPORTION`: Proportion (between 0 and 1) of cells to be alive when using the 'random' board. Defaults to 0.5.
- `-w | --wrap-around`: If set, wrap around the edges of the board (i.e. opposite edges connect to each other).
- `-f | --frame-time FRAME_TIME`: Seconds between each frame. Default is 0.1.

## Examples

```bash
$ pygol --board glider --wrap-around
┌────────────────────────────────────────────────┐
│                                                │
│      ██                                        │
│        ██                                      │
│    ██████                                      │
│                                                │
│                                                │
│                                                │
│                                                │
│                                                │
│                                                │
│                                                │
└────────────────────────────────────────────────┘

```

```bash
$ pygol --board random -a 0.4
┌────────────────────────────────────────────────────────────────┐
│██  ██    ████████  ██    ████              ██  ██          ██  │
│      ████    ████  ██        ██████████          ██  ██  ██  ██│
│██    ████  ████  ██          ██████  ██  ██        ██████████  │
│  ██  ██      ██          ████  ██  ████  ████  ██        ██████│
│        ██    ██  ████    ██    ████      ████                ██│
│      ██  ██    ██████    ██  ████      ██  ████    ██    ████  │
│    ██  ██████        ██████    ██    ████            ██    ██  │
│██          ██        ██            ████        ██████  ██      │
│██      ██          ████  ████  ██  ██████  ████        ██████  │
│  ██  ██    ██      ██    ██  ████          ██      ██  ██████  │
│      ██  ██  ██                ██  ██  ██  ████████      ██  ██│
│    ████    ██      ██      ██      ██  ██████  ██  ██          │
│    ████        ██        ██  ██  ██      ██    ██      ██    ██│
│██          ████    ██  ██████  ████      ████      ████  ██  ██│
│██  ██████████  ████  ██        ████      ██████            ██  │
│  ██    ████    ████  ████  ██  ██            ████  ████    ████│
│    ██      ██            ██  ██        ████████        ████  ██│
│          ████  ██    ██      ████  ██  ████  ████          ██  │
└────────────────────────────────────────────────────────────────┘
```

## Contributing

- Report issues and submit pull requests through Github
- Using `poetry install` when installing from source will automatically install `black`, `flake8`, `mypy`, `isort`, and `pytest`. Please use these on any files modified by your pull request.

## License

This project is licensed under the terms of the MIT license.
