.PHONY: all check community computing export clean
all: check
	python3 scripts/build.py
check:
	python3 scripts/check.py
community:
	python3 scripts/build.py 01-comunidades-abiertas
computing:
	python3 scripts/build.py 02-computacion-reproducible
export: all
	python3 scripts/export.py
clean:
	python3 scripts/clean.py
