# Equation solver by Manuel Floriano

This readme file explains some insights about how the algorithm works and how to use it.
Exercise done in `Ubuntu` operating system with Python 3.8.10. All built-in tools.

This program solves a set of equations whose format can be found
at `Format of the example file` section.

## Algorithm

The algorithm itself replicates how human solves a set of equations. It can be divided
into two main steps:

- Computing the associated cost to each symbol. This cost can be seen as a metric
  similar to the number of human steps taken to solve a given equation. For example, an
  equation as `x = 2` will have a 0 cost, but an equation like `y = x + 2` will have a
  higher cost, as this one depends on a symbol whose value we do not have a priori.
  This step is done by applying a recursive algorithm that defines the cost for all
  symbols. This algorithm makes use of pre-computed values to save some time. The time
  complexity of this step scalates linearly based on the number of equations, `O(n)`

- Solving the equations: Now that all the costs were computed, it is only necessary to
  iterate all the equations in ascending order of this metric. This order will ensure
  that, by the time an equation is reached, all the symbols needed to compute its
  solution have been previously found.
  In terms of velocity, this step only needs to traverse the array with all the
  equations once, meaning that it follows a `O(n)` time complexity, being `n` the
  number of equations.

## How to use

A default example can be used with:

```bash
python3 equation_solver/scripts/equation_solver.py
```
Or with:

```bash
pip install .
equation_solver --file-path equation_solver/data/example1.txt
```

### Format of the example file

The file admits multiple whitespaces. However, the left-hand side only admits one
single symbol that must not be repeated in other lines. Example:

```
z = x  +  5
x  = y + 2
y = 1
```

## Developer

### Testing

A few quick unit tests were writen to cover 100% of the implemented tools. To launch
them, install the package and then use `pytest` to run all of them:

```bash
# At the root of the github repo
pip install .
pytest .
```
