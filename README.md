Auction Demo
=========

Overview
--------
A lightweight python script to demo basic functions of an auction service.

Assumptions
------------------------

* If the input file does not contain any timestamp >= auction closing time, 
the auction will stay open and nothing will be printed to standard output for that given auction

Setup
-----
* Run `make install` to build the world

How to:
-------
* `make lint`: cleans up using ([black](https://pypi.org/project/black/), [flake8](https://pypi.org/project/flake8/), [mypy](https://pypi.org/project/mypy/))
* `make tests`: runs the unit tests
* `make run`: runs the script with a default input file path parameter, feel free to override using;
  - `FILE_PATH=/path/to/some/input/file.txt make run`

Development Requirements
------------------------

* [Python 3.10.0 or higher](https://www.python.org/downloads/release/python-3100/) Just for compatibility reasons make sure you have the right version of python installed, or use [pyenv](https://github.com/pyenv/pyenv)
to emulate the right python version

Troubleshooting
---------------

* If you get an error like this after installing pyenv and pointing to the right python version:
```bash
make: *** [lint] Error 1
(base) basha@Ahmeds-iMac parking % ./bin/run-black.sh

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