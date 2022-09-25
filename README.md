[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# Contacts Backend

Based on Google Contacts app on Android, this is supposed to the backend that supports such app. Supports both REST and GraphQL endpoints.

## Dev
You will need docker installed to run.

    docker-compose up

The server should be running on `http://localhost:7770`.

Open API docs on `http://localhost:7770/docs`

API docs on `http://localhost:7770/api/v1`

GraphQL on `http://localhost:7770/graphql/v1`

## Models and Migration

Create migration files

    docker-compose run --rm web aerich migrate --name "description"

Upgrade/downgrade from migration database

    docker-compose run --rm web aerich upgrade/downgrade


## GraphQL

### Register

### Login

```
mutation ($input: LoginInput!) {
  login(inputData: $input) {
    success
    accessToken
    tokenType
    error {
      text
      code
      description
    }
  }

=======
{
  "input": {
    "username": "kofi@example.com",
    "password": "examples"
  }
}
```