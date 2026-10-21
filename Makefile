.PHONY: all check community computing export pages clean
STRICT ?= 0
export STRICT
all:
	python3 scripts/build.py
check:
	python3 scripts/check.py
community:
	python3 scripts/build.py 01-comunidades-abiertas
computing:
	python3 scripts/build.py 02-computacion-reproducible
export:
	python3 scripts/export.py
pages: all
	python3 scripts/build_pages.py
clean:
	python3 scripts/clean.py
