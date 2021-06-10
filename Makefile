install:
	pipenv install

test:
	mkdir -p build
	export PYTHONPATH=./; pipenv run pytest ./tests -s --junit-xml=build/tests.xml
