"""Solve a basic set of equations by using a txt file as input."""
import argparse

from equation_solver.equation_tools import SetEquations


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create the parser, defining the different arguments."""
    parser = argparse.ArgumentParser(
        description="Provide a file with a set of equations that will be solved."
    )
    parser.add_argument(
        "--file-path",
        help="txt file containing the set of equations.",
        default="example1.txt",
    )
    return parser

def main() -> None:
    parser = _create_argument_parser()
    args = parser.parse_args()
    set_equations = SetEquations.from_txt(args.file_path)
    set_equations.solve_eq_set(display_results=True)


if __name__ == "__main__":
    main()
