build:
	python setup.py sdist bdist_wheel
install:
	pip install dist/hunter_sdk-0.1.0-py3-none-any.whl
test:
	pytest
clean:
	rm -rf dist build hunter_sdk.egg-info

isort:
	isort hunter_sdk tests
black:
	black hunter_sdk tests
flake8:
	flake8 hunter_sdk tests
ruff:
	ruff format

format: flake8 ruff

mypy:
	mypy .

full_test:  format test mypy