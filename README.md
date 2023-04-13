Parking Lot Problem
===================

Overview
--------
A lightweight python script to demo basic functions of a parking lot service.

Assumptions
-----------

* Parking spots are assigned sequentially: The implementation assumes that parking spots are assigned sequentially, 
i.e., the lowest available spot number is assigned to an incoming vehicle. This simplifies the process of finding 
an available parking spot.
* Parking tickets are unique and sequential: The Ticket class assumes that ticket numbers are unique and assigned 
sequentially. This simplifies the process of tracking parked vehicles and their corresponding tickets.
* Fee models are pre-defined: The implementation assumes that fee models are pre-defined for each parking lot, 
and the applicable fees can be calculated based on these models.
* The parking duration is always positive: The implementation assumes that the parking duration is always positive, 
i.e., a vehicle cannot be unparked before it was parked. This means that the implementation doesn't handle cases where 
the entry and exit timestamps are invalid or reversed.

Setup
-----
* Run `make install` to build the world

How to:
-------
* `make lint`: cleans up using ([black](https://pypi.org/project/black/), [flake8](https://pypi.org/project/flake8/), [mypy](https://pypi.org/project/mypy/))
* `make tests`: runs the unit tests
* `make run`: runs the script with a default input file path parameter, feel free to override using;
  - :warning: Make sure to run `poetry config virtualenvs.in-project true` prior, so the virtual env lives within the project directory

Development Requirements
------------------------

* [Pyenv](https://github.com/pyenv/pyenv) if you want to emulate different versions of python instead of overriding the installed python on your machine
* [Python 3.10.0 or higher](https://www.python.org/downloads/release/python-3100/) Just for compatibility reasons make sure you have the right version of python installed
* [Poetry](https://python-poetry.org/) as a package dependency management solution

Troubleshooting
---------------

* If you get an error like this after installing pyenv and pointing to the right python version:
```bash
make: *** [lint] Error 1
(base) basha@Ahmeds-iMac park-it % ./bin/run-black.sh

Current Python version (3.9.12) is not allowed by the project (^3.10).
Please change python executable via the "env use" command.
```
Then try running these commands in the root:
```bash
$ rm -rf .venv
$ pyenv local 3.10.0
$ poetry env use 3.10.0
$ make install
```
This forces poetry to look at the pyenv version instead