export PYTHONPATH := $(shell pwd)

install:
	@poetry install
	@poetry run pre-commit install -f

update:
	@poetry update
	@poetry run pre-commit autoupdate

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./django_microsoft_sso

lint:
	@poetry run pre-commit run --all
