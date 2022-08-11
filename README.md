# Contacts Backend

Based on Google Contacts app on Android, this is supposed to the backend that supports such app. Supports both REST and GraphQL endpoints.

## Dev
You will need docker installed to run.

    docker-compose up

The server should be running on `http://localhost:7770`.

Open API docs on `http://localhost:7770/docs`

GraphQL on `http://localhost:7770/graphql`

## Models and Migration

Create migration files

    docker-compose run --rm web aerich migrate --name "description"

Upgrade/downgrade from migration database

    docker-compose run --rm web aerich upgrade/downgrade