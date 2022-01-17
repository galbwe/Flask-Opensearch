*Currently under development*

# Flask Opensearch

A minimal flask extension that provides compatibility with the opensearch python client.

# Development

To set up a development environment, you need to install Docker and Docker-Compose. Please see https://www.docker.com/products/docker-desktop for installation instructions.

Once you have Docker and Docker-Compose installed, you can create a development environment by running the following commands:

```
# Create a new development environment with Docker-Compose and run the tests
docker compose up --build
```

If you have already build the docker images and just want to run the tests, you can run the following command:

```
docker compose exec testenv tox
```


When you are done developing, you can stop the development environment by running:

```
docker compose down
```