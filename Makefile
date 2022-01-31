VENV = venv
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip3

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_dir_full_path := $(abspath $(current_dir))


# -----------------------------------------------------------------------------
# LOCAL USAGE

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


# Loads the initial data
load_init_data: install
	${PYTHON} web/manage.py load_campaigns -f "data/campaigns.csv"
	${PYTHON} web/manage.py load_ad_groups -f "data/adgroups.csv"
	${PYTHON} web/manage.py load_search_terms -f "data/search_terms.csv"


# Load campaign data
load_campaigns: install
	${PYTHON} web/manage.py load_campaigns

# Load ad group data
load_ad_groups: install
	${PYTHON} web/manage.py load_ad_groups

# Load search term data
load_search_terms: install
	${PYTHON} web/manage.py load_search_terms


# -----------------------------------------------------------------------------
# DOCKER USAGE

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

# Loads the initial data from the docker container
docker-load-init-data:
	docker cp data ${current_dir}_web_1:/tmp/.
	docker exec ${current_dir}_web_1 ./manage.py load_campaigns -f /tmp/data/campaigns.csv
	docker exec ${current_dir}_web_1 ./manage.py load_ad_groups -f /tmp/data/adgroups.csv
	docker exec ${current_dir}_web_1 ./manage.py load_search_terms -f /tmp/data/search_terms.csv
	rm -rf /tmp/data

# Load campaign data from the docker container
docker-load-campaigns:
	docker exec -i ${current_dir}_web_1 ./manage.py load_campaigns

# Load ad group data from the docker container
docker-load-ad-groups:
	docker exec -i ${current_dir}_web_1 ./manage.py load_ad_groups

# Load search term data from the docker container
docker-load-search-terms:
	docker exec -i ${current_dir}_web_1 ./manage.py load_search_terms
