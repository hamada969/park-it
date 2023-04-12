.PHONY: install \
        tests \
		lint \
		run

install:
	poetry install

lint:
	bin/run-black.sh && \
    bin/run-flake8.sh && \
    bin/run-mypy.sh

tests:
	poetry run pytest

# path to the input test file.  can be overriden.
FILE_PATH ?= $(shell realpath input.txt)

run: install
	poetry run python -m parking $(FILE_PATH)