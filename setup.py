from setuptools import find_packages, setup

setup(
    name="equation_tools",
    version="0.0.1",
    maintainer="mflova",
    python_requires=">=3.8",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "equation_solver=equation_solver.scripts.solver:main",
        ]
    },
    zip_safe=False,
)
