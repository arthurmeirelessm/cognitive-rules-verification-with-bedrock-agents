.PHONY: format lint

format:
	black src/
	isort src/

lint:
	flake8 src/

check: format lint
