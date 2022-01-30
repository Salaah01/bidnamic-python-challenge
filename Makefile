VENV = venv
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip3

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

# Create virtual environment
venv:
	python3 -m venv venv

# Install dependencies
install: venv web/requirements.txt web/requirements.dev.txt
	${PIP} install -r web/requirements.dev.txt


# Runs migrations and runs server
runserver: install
	${PYTHON} web/manage.py migrate
	${PYTHON} web/manage.py runserver


# Runs tests locally
test: install
	${PYTHON} web/manage.py test

# Runs formatter
format: install
	${PYTHON} -m black web/.

# Run liniter
lint: install
	${PYTHON} -m flake8 web/


# Builds docker image
docker-build:
	docker-compose build

# PIP install requirements
docker-pip-install: web/requirements.txt web/requirements.dev.txt
	docker exec ${current_dir}_web_1 pip install -r /app/requirements.dev.txt

# Runs docker image
docker-up:
	docker-compose up -d

# Stops docker image
docker-down:
	docker-compose down

# Runs tests from the docker container
docker-test:
	docker exec ${current_dir}_web_1 ./manage.py test

# Runs formatter from the docker container
docker-format:
	docker exec ${current_dir}_web_1 black . --line-length 79

# Runs liniter from the docker container
docker-lint:
	docker exec ${current_dir}_web_1 flake8 .
