install:
	pipenv install

build:
	./setup.py build

test:
	mkdir -p build
	export PYTHONPATH=./; pipenv run pytest ./tests -s --junit-xml=build/tests.xml

release:
	twine upload --disable-progress-bar --verbose \
		--username=__token__ \
		--password=${PYPI_TOKEN} \
		--skip-existing \
		dist/*
