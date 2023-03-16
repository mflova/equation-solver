"""Module to test the methods from `equation_tools`."""
import os
from typing import Final, Mapping

import pytest

from equation_solver.tools.structures import Equation, EquationError, SetEquations


class TestEquation:
    """Tests for the `Equation` class."""

    @pytest.mark.parametrize(
        "string, expected_equation",
        [
            ("x = 7 + y", Equation("x", {"y"}, 7)),  # Simple case
            ("offset = roll + 1", Equation("offset", {"roll"}, 1)),  # Multi-char vars
            ("x =   roll +   1", Equation("x", {"roll"}, 1)),  # Multiple spaces
            ("x = 2  + z +  1", Equation("x", {"z"}, 3)),  # Multiple constants
            ("x = 1 + y + z ", Equation("x", {"z", "y"}, 1)),  # Multiple unknowns
            (" x  = 1 + y  + z ", Equation("x", {"z", "y"}, 1)),  # More spaces
        ],
    )
    def test_instantiate_from_string(
        self, string: str, expected_equation: Equation
    ) -> None:
        """
        Verify that `Equation` can be correctly instantiated from a string.

        :param string: Any string that represents an equations.
        :param expected_equation: Expected `Equation` object that will be instantiated
            if `string` is provided.
        """
        assert expected_equation == Equation.from_string(string)

    def test_solve_equation_exceptions(self) -> None:
        """Test that exceptions are triggered when not enough unknowns are provided."""
        equation = Equation("z", {"x", "y"}, 2)
        with pytest.raises(EquationError):
            equation.solve_equation({"w": 3, "x": 5})

    @pytest.mark.parametrize(
        "equation, unknowns_provided, expected_solution",
        [
            (Equation("x", {"y"}, 7), {"y": 2}, 9),
            (Equation("x", {"y", "z"}, 2), {"y": 2, "z": 1}, 5),
            (Equation("z", {"y", "offset"}, 7), {"y": 2, "offset": 10}, 19),
        ],
    )
    def test_solve_equation(
        self,
        equation: Equation,
        unknowns_provided: Mapping[str, int],
        expected_solution: int,
    ) -> None:
        """
        Verify that the equation solved computes the expected output.

        For this test, multiple different equations are provided.

        :param equation: `Equation` object.
        :param unknowns_provided: Unknowns that will be provided to solve
            the `equation` object.
        :param expected_solution: Solution that should be find after
            the `unknowns_provided` are used as input to `solve_equation`.
        """
        solution = equation.solve_equation(unknowns_provided)
        assert solution == expected_solution


class TestSetEquations:
    """Tests for the `SetEquations` class."""

    TEST_DATA_DIR: Final = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    """Directory where the tests are located."""
    EXAMPLE_FILE: Final = os.path.join(TEST_DATA_DIR, "example1.txt")
    """Path to an example file for testing purposes."""

    def test_from_txt(self) -> None:
        """
        Verify that the class can be instantiated from an generic txt file.

        This test verifies that nothing breaks and that the symbols are correctly loaded.
        """
        set_equations = SetEquations.from_txt(self.EXAMPLE_FILE)
        assert set_equations.symbols == {"x", "y"}

    @pytest.mark.parametrize(
        "equations_dct, expected_costs",
        [
            (
                {
                    "x": Equation.from_string("x = y + 4"),
                    "y": Equation.from_string("y = 1"),
                    "z": Equation.from_string("z = x + 2"),
                },
                {"x": 1, "y": 0, "z": 2},
            ),
        ],
    )
    def test_compute_cost(
        self, equations_dct: Mapping[str, Equation], expected_costs: Mapping[str, int]
    ) -> None:
        """
        Verify that the expected cost is well computed.

        :param equations_dct: Dictionary used to instantiate `SetEquation`
        :param expected_costs: Dictionary storing the expected equation costs for this
            set of equations.
        """
        set_equations = SetEquations(equations_dct)
        set_equations._compute_all_symbols_cost()
        for symbol, expected_cost in expected_costs.items():
            assert set_equations._symbol_cost[symbol] == expected_cost

    @pytest.mark.parametrize(
        "equations_dct, expected_solutions",
        [
            (
                {
                    "x": Equation.from_string("x = y + 1"),
                    "y": Equation.from_string("y = 1"),
                },
                {"x": 2, "y": 1},
            ),
            (
                {
                    "x": Equation.from_string("x = y + 4"),
                    "y": Equation.from_string("y = 1"),
                    "z": Equation.from_string("z = x + 2"),
                },
                {"x": 5, "y": 1, "z": 7},
            ),
        ],
    )
    def test_solve_eq_set(
        self, equations_dct: Mapping[str, Equation], expected_solutions: Mapping[str, int]
    ) -> None:
        """
        Verify that the solutions are the correct ones given a few examples.

        :param equations_dct: Dictionary used to instantiate `SetEquation`
        :param expected_solutions: Dictionary containing the expected solutions of the
            equation.
        """
        set_equations = SetEquations(equations_dct)
        # `display_results` set to `True` just to verify that the code does not break
        # when printing the results.
        assert expected_solutions == set_equations.solve_eq_set(display_results=True)
