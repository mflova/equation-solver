# Equation solver by Manuel Floriano

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

## How to use

A default example can be used with:

```bash
python3 main.py
```

But more examples can be tested with:

```bash
python3 main.py --file <path_to_file.txt>
```

## Testing

Given the type of this vacancy, a few quick unit tests (14) were writen to cover 100%
of the written tools. It is only needed `pytest`. You only need to execute this line in
the root directory of the exercise:

```bash
pip install pytest
pytest .
```

Note: Instead of creating a `setup.py` and to ease the review of the exercise, I
manually added the root directory from `test_equation_tools` to the `sys.path` so that
I can import the tools I created. I am aware this is not a good practice at all. I
usually create a `setup.py` for this.
