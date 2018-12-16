TESTS_DIR = ./testes/


install-dev:
	@pip install --upgrade --force-reinstall -e .

install-prod:
	@pip install --upgrade --force-reinstall

test:
	@py.test --rootdir=$(TESTS_DIR)

cov:
	@py.test --cov-report term-missing --cov=imdb $(TESTS_DIR)
	@rm -f ./media/coverage.svg
	@coverage-badge -o ./media/coverage.svg

pep8:
	@autopep8 -r -i ./imdb
	@pycodestyle ./imdb --show-source --statistics --count

clear: clean

clean:
	@rm -fr .pytest_cache
	@rm -fr .eggs/
	@rm -f .coverage
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +
