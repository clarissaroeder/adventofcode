import argparse
import importlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AOC")
    parser.add_argument("day", type=int, help="Day number to run")
    parser.add_argument(
        "--input",
        "-i",
        default="example.txt",
        help="Input file to load (default: example.txt)",
    )
    parser.add_argument(
        "--part",
        "-p",
        type=int,
        help="Part 1 or 2 of puzzle"
    )
    args = parser.parse_args()

    try:
        module_name = f"day_{args.day}.solution"
        Advent = getattr(importlib.import_module(module_name), "Advent")
        advent = Advent(args.input, args.part)
        advent.solve()

    except ModuleNotFoundError:
        print(f"No solution implemented for day {args.day}.")
