install:
	pipenv install

build:
	./setup.py build

test:
	mkdir -p build
	export PYTHONPATH=./; pipenv run pytest ./tests -s --junit-xml=build/tests.xml
