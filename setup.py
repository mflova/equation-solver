from setuptools import setup, find_packages

setup(name="equation_solver",
      version="1.0",
      description="Solve a set of equations",
      author="Manuel Floriano Vázquez",
      url="www.github.com/mflova",
      packages=find_packages(),
      package_data={"": ["datasets/*.txt"]},
      entry_points={
          "console_scripts": [
              "equation_solver = equation_solver.scripts.main:main",
          ],
      }
     )
