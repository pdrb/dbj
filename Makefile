lint:
	ruff check
	ruff check --select I --fix
	ruff format

test:
	python3 -m unittest -v

build:
	python3 -m build

clean:
	rm -rf dist
	find . -name '.ruff_cache' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
