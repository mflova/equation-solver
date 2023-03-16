# Equation solver

This readme file explains some insights about how the algorithm works and how to use it.
Tested in `Ubuntu` operating system with Python 3.8.10. All built-in tools.

## Description

This program evaluates a set of equations defined on separate lines. These equations
are defined by:

- Left-hand side: Must be a variable name
- Right-hand side: Whose side can be composed of integers, variables and the addition
  operator.

Equations might contain flexible format, which means that multiple whitespaces are allowed.

Example:

```
z = 1 +  w + 2
y   = 37
k  = offset + z
offset =  10
x = y
w =   x +  46
```

## Algorithm

The algorithm itself replicates how human solves a set of equations. It can be divided
into two main steps:

- Computing the associated cost to each symbol. This cost can be seen as a metric
  similar to the number of human steps taken to solve a given equation. For example, an
  equation as `x = 2` will have a 0 cost, but an equation like `y = x + 2` will have a
  higher cost, as this one depends on a symbol whose value we do not have a priori.
  This step is done by applying a recursive algorithm that defines the cost for all
  symbols. This algorithm makes use of pre-computed values to save some time.

- Solving the equations: Now that all the costs were computed, it is only necessary to
  iterate all the equations in ascending order of this metric. This order will ensure
  that, by the time an equation is reached, all the symbols needed to compute its
  solution have been previously found.
  In terms of velocity, this step only needs to traverse the array with all the
  equations once, meaning that it follows a `O(n)` time complexity.

## Using

### As a script

In order to use this application as a pip package, it only needs to be installed with:

```bash
pip install .
```

And then it can be used as:

```bash
equation_solver # It will use default dataset
equation_solver --file <path_to_file.txt>
```

## Testing

A few quick unit tests were written to cover 100% of the written tools. Install the
package as developper and run pytest:

```bash
pip insatll .[dev]
pytest .
```

## Pipeline

In order to maintain good quality code, following tools are used in the pipeline:

- [Flake8](https://flake8.pycqa.org/en/latest/): Linting tool.
- [Pylint](https://github.com/PyCQA/pylint): Linting tool similar to Flake8.
- [Codespell](https://github.com/codespell-project/codespell): Linting tool to verify
  there are not any misspell.
- [Mypy](https://www.mypy-lang.org/): Static analysis tool that enforces correct type
  hints.
- [Pytest](https://docs.pytest.org/en/7.2.x/): Tool used to run and verify multiple
  unit test.
