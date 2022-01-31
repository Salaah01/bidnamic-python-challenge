#!/usr/bin/env bash
# Creates a postgres database and user for the application with the
# configurations set in `web/.env`.

set -e

# Check if psql is installed
if ! command -v psql >/dev/null; then
  echo "psql is not installed. Please install it and try again."
  exit 1
fi

# Check that the .env file exists
if [ ! -f "web/.env" ]; then
  echo "web/.env file does not exist. Please create it and try again."
  exit 1
fi

# Read the environment variables from the .env file
. web/.env

# Create the user if it doesn't exist
if ! psql -c "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
  psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD'"
fi

# Create the database if it doesn't exist
if ! psql -c "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
  psql -c "CREATE DATABASE $DB_NAME"
fi

# Grant the user permissions to the database
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER"
