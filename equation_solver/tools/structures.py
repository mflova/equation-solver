"""Tools used to work with mathematical equations."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, KeysView, Mapping, Set


class EquationError(Exception):
    """Exception raised whenever there is a problem with the equations."""


@dataclass
class Equation:
    """
    Class that holds the representation of an equation.

    For the following exercise, all equations can be represented as:
    `symbol` = `sum_constants` + sum(`unknowns`)
    """

    symbol: str
    """Symbol found in the LHS."""
    unknowns: Set[str]
    """Multiple unknowns that define the equation."""
    sum_constants: int
    """Result of the sumation of all constants in the equation."""

    @classmethod
    def from_string(cls, string: str) -> Equation:
        """
        Instantiate the equation from a given string.

        This assumes that the format of this equation is the following one: `LHS` = `RHS`
        Where `LHS` contains a single symbol and `RHS` contains other multiple symbols
        and constants. All of them with `+` operator.

        :param string: Single string containing the information to parse the equation.
        :return: Object of `Equation` type.
        """
        substr_lst = string.strip().split(" ")

        unknowns = set()
        sum_constants = 0
        symbol = substr_lst[0]

        for substr in substr_lst[1:]:
            if substr:
                if substr.isnumeric():
                    sum_constants += int(substr)
                elif substr.isalpha():
                    unknowns.add(substr)
        return cls(symbol, unknowns, sum_constants)

    def solve_equation(self, unknowns_provided: Mapping[str, int]) -> int:
        """
        Solve the equation stored in this object.

        This method assumes that the equation has a valid solution.

        :param unknowns_provided: Dictionary mapping the symbol provided (key) with the
            value assigned to it (value). These values will be used to replace all the
            unknowns in the equation and to later find out the solution.
        :return: Numeric value with the solution found.
        :raises EquationError: When not all required unknowns were provided.
        """
        if not self.unknowns.issubset(unknowns_provided.keys()):
            raise EquationError(
                f"Not all unknowns in the equation `{self}` have been provided "
                f"as input to this method (`{unknowns_provided.keys()}`)"
            )

        sum_unknowns = 0
        for unknown, value in unknowns_provided.items():
            if unknown in self.unknowns:
                sum_unknowns += value
        return self.sum_constants + sum_unknowns

@dataclass
class SetEquations:
    """Hold and perform multiple operations related to a set of equations."""

    equations: Mapping[str, Equation]
    """Map each symbol to its corresponding associated equation."""

    _symbol_cost: Dict[str, int] = field(default_factory=dict, init=False)
    """Estimated cost that each symbol takes to solve."""

    @classmethod
    def from_txt(cls, path: str) -> SetEquations:
        """
        Instantiate a set of equations from a txt file provided.

        :param path: Path to the txt file.
        :return: Object of type `SetEquations`.
        """
        with open(path) as f:
            content = f.read()
        equation_strs = content.split("\n")
        dct_equations = {}
        for equation_str in equation_strs:
            if equation_str:
                equation = Equation.from_string(equation_str)
                dct_equations[equation.symbol] = equation
        return cls(dct_equations)

    def solve_eq_set(self, display_results: bool = False) -> Mapping[str, int]:
        """
        Solve the set of equations previously stored in this object.

        This method previously calculates the complexity of each equation by taking
        into account the dependencies among different symbols. Then, all of them are
        solved in increasing order of complexity, which will guarantee that all symbols
        are avaialble when solving a new equation.

        :param display_results: `True` to print the results, `False` otherwise.
            Defaults to False
        """
        solutions: Dict[str, int] = {}
        self._compute_all_symbols_cost()
        for symbol in self._symbol_cost:
            pointed_eq = self.equations[symbol]
            if pointed_eq.unknowns:
                solutions[symbol] = pointed_eq.solve_equation(solutions)
            else:
                solutions[symbol] = pointed_eq.sum_constants
        if display_results:
            self._print_solutions(solutions)
        return solutions

    def _print_solutions(self, solutions: Mapping[str, int]) -> None:
        """
        Print the solutions with the specified format.

        :param solutions: Dictionary mapping the symbol and its value found.
        """
        # Order the dictionary by its key
        sorted_solutions = {key: value for key, value in sorted(solutions.items())}
        for symbol, value in sorted_solutions.items():
            print(f"{symbol} = {value}")

    def _compute_all_symbols_cost(self) -> None:
        """
        Update `_symbol_cost` cache with the cost it takes to solve each symbol.

        This cost evaluate the dependencies among all the symbols and assigns a
        complexity-based score to each equation. Ordered in ascending complexity.
        """
        for symbol in self.symbols:
            self._compute_symbol_cost(symbol)

        # Order the dictionary by its value once all of the are computed
        self._symbol_cost = {k: v for k,v in sorted(self._symbol_cost.items(), key=lambda item: item[1])}

    def _compute_symbol_cost(self, symbol: str) -> int:
        """
        Recursive-based method that calculates the cost for a single symbol.

        All intermediate costs found are stored in `_symbol_cost`
        The complexity of a symbol is determined by the score of the symbols in the RHS.

        :param symbol: Symbol whose cost will be computed.
        :return: Integer representing the cost to find out the value of that specified
            symbol.
        """
        if symbol in self._symbol_cost:
            return self._symbol_cost[symbol]

        if not self.equations[symbol].unknowns:
            self._symbol_cost[symbol] = 0
            return 0

        total_cost = 0
        for symbol_dependency in self.equations[symbol].unknowns:
            total_cost += self._compute_symbol_cost(symbol_dependency) + 1
            self._symbol_cost[symbol] = total_cost
        return total_cost

    @property
    def symbols(self) -> KeysView[str]:
        """
        Get all the symbols that need to be solve for this set of equations.

        :return: Symbols as a `KeysView`, which behaves similar to a `set`.
        """
        return self.equations.keys()
