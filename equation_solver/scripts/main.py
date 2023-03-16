"""Solve a basic set of equations by using a txt file as input."""
import argparse
import os
from typing import Final

from equation_solver.tools.structures import SetEquations

REL_DEFAULT_DATASET_PATH = "../datasets/example1.txt"
"""Relative path to the default dataset."""


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create the parser, defining the different arguments."""
    abs_dataset_path: Final = os.path.join(
        os.path.join(os.path.dirname(__file__), (REL_DEFAULT_DATASET_PATH))
    )

    parser = argparse.ArgumentParser(
        description="Provide a file with a set of equations that will be solved."
    )
    parser.add_argument(
        "--file_path",
        help="txt file containing the set of equations.",
        default=abs_dataset_path,
    )
    return parser


def main() -> None:
    """Read and solve the equation."""
    parser = _create_argument_parser()
    args = parser.parse_args()
    set_equations = SetEquations.from_txt(args.file_path)
    set_equations.solve_eq_set(display_results=True)


if __name__ == "__main__":
    main()
