"""Install the whole package."""
from setuptools import setup, find_packages

setup(
    name="equation_solver",
    version="1.0",
    description="Solve a set of equations",
    author="Manuel Floriano Vázquez",
    url="www.github.com/mflova",
    packages=find_packages(),
    package_data={"": ["datasets/*.txt"]},
    extras_require={
        "dev": [
            "pytest==7.2.1",
            "types-setuptools==67.6.0.0",
            "mypy==0.991",
            "flake8==5.0.4",
            "codespell==2.2.2",
            "pylint==2.15.10",
        ]
    },
    entry_points={
        "console_scripts": [
            "equation_solver = equation_solver.scripts.main:main",
        ],
    },
)
