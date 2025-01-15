build:
	python setup.py sdist bdist_wheel
install:
	pip install dist/hunter_sdk-0.1.0-py3-none-any.whl
test:
	pytest
clean:
	rm -rf dist build hunter_sdk.egg-info

isort:
	isort hunter_sdk tests --check
black:
	black hunter_sdk tests --check
flake8:
	flake8 hunter_sdk tests
