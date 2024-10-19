import argparse
import curses
import os
from time import sleep

from .board import Board

script_dir = os.path.dirname(os.path.abspath(__file__))

boards_dir = os.path.join(script_dir, 'boards')

DEFAULT_BOARD = 'beacon'
DEFAULT_FRAME_TIME = 0.1
DEFAULT_ALIVE_PROPORTION = 0.5


def draw_frame(stdscr, current_frame: str, previous_frame: str = None):
    height, width = stdscr.getmaxyx()
    lines = current_frame.splitlines()

    if previous_frame:
        prev_lines = previous_frame.splitlines()
    else:
        prev_lines = [""] * len(lines)  # Dummy empty frame

    if len(lines) > height:
        lines = lines[:height]

    for i, (line, prev_line) in enumerate(zip(lines, prev_lines)):
        if line != prev_line:  # Only redraw lines that have changed
            if len(line) > width:
                line = line[:width]
            try:
                stdscr.addstr(i, 0, line)
            except curses.error:
                pass
    stdscr.refresh()


def pygol(stdscr, args):
    curses.curs_set(0)

    frame_time = args.frame_time

    if args.board == "random":
        board = Board(wrap_around=args.wrap_around).random_state(32, 18, 1 - args.alive_proportion)
    else:
        board_file = args.input if args.board == "custom" else os.path.join(boards_dir, f"{args.board}.txt")
        board = Board(wrap_around=args.wrap_around).load_board_from_file(board_file)

    while True:
        draw_frame(stdscr, str(board))
        board.iterate_state()
        sleep(frame_time)


def main():
    parser = argparse.ArgumentParser(description="A simple CLI simulator for Conway's Game of Life.")
    board_choices = [x[:-4] for x in os.listdir(boards_dir)]
    board_choices = [*board_choices, "custom", "random"]
    parser.add_argument(
        "-b",
        "--board",
        choices=board_choices,
        default=DEFAULT_BOARD,
        help=f"The starting board to simulate. If set to custom, you must specify an input file. Default is '{DEFAULT_BOARD}'.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="A txt file of 1s and 0s arranged in rows representing a starting board. Only applies to the 'custom' board.",
    )
    parser.add_argument(
        "-a",
        "--alive-proportion",
        type=float,
        default=DEFAULT_ALIVE_PROPORTION,
        help=f"""Proportion (between 0 and 1) of cells to be alive.
        Only applies to the 'random' board. Defaults to {DEFAULT_ALIVE_PROPORTION}.""",
    )
    parser.add_argument(
        "-w",
        "--wrap-around",
        action="store_true",
        help="Wrap around the edges of the board (i.e. opposite edges connect to each other).",
    )
    parser.add_argument(
        "-f",
        "--frame-time",
        type=float,
        default=DEFAULT_FRAME_TIME,
        help=f"Seconds between each frame. Default is {DEFAULT_FRAME_TIME}.",
    )

    args = parser.parse_args()

    if args.board == "custom" and args.input is None:
        raise ValueError("If using custom board, you must specify an input file!")

    if args.board == "random" and (args.alive_proportion < 0 or args.alive_proportion > 1):
        raise ValueError("Alive proportion must be between 0 and 1!")

    if args.frame_time < 0:
        raise ValueError("Frame time must be positive!")

    curses.wrapper(pygol, args)


if __name__ == "__main__":
    main()
