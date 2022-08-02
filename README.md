# Contacts Backend

REST GraphQL backend for contacts app.

## Models

# Migration

Create migration files

    docker-compose run --rm web aerich migrate --name "description"

Upgrade/downgrade from migration database

    docker-compose run --rm web aerich upgrade/downgrade