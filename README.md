Parking Lot Problem
===================

Overview
--------
A lightweight python script to demo basic functions of a parking lot service.

Assumptions
-----------

* ....

Setup
-----
* Run `make install` to build the world

How to:
-------
* `make lint`: cleans up using ([black](https://pypi.org/project/black/), [flake8](https://pypi.org/project/flake8/), [mypy](https://pypi.org/project/mypy/))
* `make tests`: runs the unit tests
* `make run`: runs the script with a default input file path parameter, feel free to override using;
  - `FILE_PATH=/path/to/some/input/file.txt make run`
  - :warning: Make sure to run `poetry config virtualenvs.in-project true` prior, so the virtual env lives within the project directory

Development Requirements
------------------------

* [Pyenv](https://github.com/pyenv/pyenv) if you want to emulate different versions of python instead of overriding the installed python on your machine
* [Python 3.11.0 or higher](https://www.python.org/downloads/release/python-3100/) Just for compatibility reasons make sure you have the right version of python installed
* [Poetry](https://python-poetry.org/) as a package dependency management solution

Troubleshooting
---------------

* If you get an error like this after installing pyenv and pointing to the right python version:
```bash
make: *** [lint] Error 1
(base) basha@Ahmeds-iMac park-it % ./bin/run-black.sh

Current Python version (3.9.12) is not allowed by the project (^3.11).
Please change python executable via the "env use" command.
```
Then try running these commands in the root:
```bash
$ rm -rf .venv
$ poetry env use 3.11.0
$ poetry install
```
This forces poetry to look at the pyenv version instead