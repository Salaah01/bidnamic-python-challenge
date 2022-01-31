# Bidnamic API

The Bidnamic API is a RESTful API that allows you to retrieve data on top search terms by RoAS by campaign `structure_value` or ad group `alias`.
This documentation is intended for end-users and developers.

## Requirements
* Python >=3.8
* PostGreSQL >=10.1
* Docker (optional) - This would greatly speed up the deployment time.
* Docker Compose (optional) - This would greatly speed up the deployment time.

## Installation

### Docker
If you have `Docker` and `Docker Compose` installed, you can follow these steps to install the application.

1. Set docker environment variables.
Docker will read environment variables from `web/.docker.env`. You can copy `web/docker.sample.env` to `web/.docker.env` and replace the values with your own.
The following variables are required:

| Variable    | Description       |
| ----------- | ----------------- |
| SECRET_KEY  | Django secret key |
| DB_NAME     | Database name     |
| DB_USER     | Database user     |
| DB_PASSWORD | Database password |
| DB_PORT     | Database port     |

2. Set up postgres environment variable.
Docker will expect `.postgres.env` to exist with variables to setup your postgres database. You can copy `postgres.sample.env` to `.postgres.env` and replace the values with your own.
The following variables are required:

| Variable          | Description       |
| ----------------- | ----------------- |
| POSTGRES_USER     | Postgres user     |
| POSTGRES_PASSWORD | Postgres password |
| POSTGRES_DB       | Postgres database |

Ensure that the database variables set in `.docker.env` and `.postgres.env` match each other. Otherwise, the web application will fail to start as it will not be able to connect to the database.

3. Build the docker containers by running `make docker-build`.
4. Start the docker containers by running `make docker-up`.
5. On the first run, if you want to load the initial data, run `docker-load-init-data`.
6. You can now navigate to `http://localhost` to get started. Here you will find instructions on how to use the API.

When you are done, you can stop the containers by running `make docker-down`.

### Manual Installation
1. Run `make install` to create a virtual environment and install the dependencies.
2. Create a file to store the environment variables in `web/.env`. You can copy `web/env.sample.env` to `web/.env` and replace the values with your own.

| Variable    | Description       |
| ----------- | ----------------- |
| SECRET_KEY  | Django secret key |
| DB_NAME     | Database name     |
| DB_USER     | Database user     |
| DB_PASSWORD | Database password |
| DB_PORT     | Database port     |

3. If a database does not exist with the environment variables set in `.env`, run `./db-setup.sh`. When running this script, you will need to ensure that you have access to `psql`.
4. Run `make runserver` to setup the database tables (migrations) and run the web application locally.
5. Press `CTRL + C` to stop the web application and run `make load_init_data` to load the initial data.
6. Run `make runserver` again to run the web application.
7. Navigate to `http://localhost:8000` to get started. Here you will find instructions on how to use the API.

When you are done, you can stop the web application by pressing `CTRL + C`.

## Loading Additional Data
Should you wish you load additional data into the database, you can run some Django management commands to load data. Each of these commands load data to a specific table and once run they will each ask you for the path a file to load. Currently, only data from csv files can be loaded.

### Docker
Before running any commands, you need to ensure that the csv you wish to load from is in the `web` container.
See [this guide](https://docs.docker.com/engine/reference/commandline/cp/) to learn how to copy files to a container.

To load data, select the relevant command based on the table you wish to load data onto and whether or not you are using Docker:

| Table        | Docker Command         | Manual Command           |
| ------------ | ---------------------- | ------------------------ |
| Campaigns    | make load-campaigns    | docker-load-campaigns    |
| Ad Groups    | make load-ad-groups    | docker-load-ad-groups    |
| Search Terms | make load-search-terms | docker-load-search-terms |

Once you have run the command, it will ask you for a path to the csv file you wish to load. Enter this path and press enter. Assuming the file exists, it will begin the upload process.

## Development

## Linting
`flake8` is installed as a linter. To run it, run the following command:

**Using Docker**
```bash
make docker-lint
```

**Manual**
```bash
make lint
```

## Formatting

`autopep8` and `black` are installed as formatters.

`autopep8` allows you to format your code according to PEP8. In Visual Studio Code, you can run this by pressing:

**Windows:** `SHIFT + ALT + F`
**MAC:** `SHIFT + OPTION + F`
**LINUX:** `SHIFT + CTRL + I`

`black` will check through your code and format it. To run this formatter, run the following command:

**Using Docker**
```bash
make docker-format
```

**Manual**
```bash
make format
```

## Testing
To run the tests, run the following command:

**Using Docker**
```bash
make docker-test
```

**Manual**
```bash
make test
```
