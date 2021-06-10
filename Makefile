install:
	command -v pipenv > /dev/null || pip install pipenv
	pipenv install

build:
	./setup.py build
	./setup.py sdist

test:
	mkdir -p build
	export PYTHONPATH=./; pipenv run pytest ./tests -s --junit-xml=build/tests.xml

release:
	pipenv run twine upload --disable-progress-bar --verbose \
		--username=__token__ \
		--password=${PYPI_TOKEN} \
		--skip-existing \
		dist/*
