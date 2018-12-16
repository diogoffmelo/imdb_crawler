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