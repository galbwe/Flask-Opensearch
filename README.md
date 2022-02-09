# Flask Opensearch

A minimal flask extension that provides compatibility with the opensearch python client.

# Quick Start

First run opensearch in a docker container. If you are working with an AWS Opensearch instance, skip this step.

```bash
docker run --name opensearch -p 9200:9200 -p 9600:9600 -e discovery.type=single-node opensearchproject/opensearch:1.0.0
```

Now in your python code, create a flask application and initialize the extension:

```python
from flask import Flask
from flask_opensearch import FlaskOpenSearch

app = Flask(__name__)

app.config["OPENSEARCH_HOST"] = "localhost"
app.config["OPENSEARCH_USER"] = "admin"
app.config["OPENSEARCH_PASSWORD"] = "admin"

opensearch = FlaskOpenSearch(
    app=app,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)
```

The keyword parameters to the `FlaskOpenSearch` constructor other than `app` are as documented in the [opensearch-py documentation](https://github.com/opensearch-project/opensearch-py).


The `opensearch` object now behaves like an opensearch-py client. For example, we can create an index, insert a document, and search for it.

```python
# Normally this code would appear in a view function, where an app context is already pushed.
with app.app_context():

    # Check that the client can connect to the opensearch instance.
    connected = opensearch.ping()
    print(connected)  # True

    # Create an index.
    res_1 = opensearch.create_index("test")
    print(res_1)
    # {'acknowledged': True, 'shards_acknowledged': True, 'index': 'test-index'}

    # Insert a document
    res_2 = opensearch.index(
        "test-index",
        body={
            'title': 'Moneyball',
            'director': 'Bennett Miller',
            'year': '2011'
        },
        id="1",
        refresh=True,
    )
    print(res_2)
    # {'_index': 'test-index',
    #     '_type': '_doc',
    #     '_id': '1',
    #     '_version': 1,
    #     'result': 'created',
    #     'forced_refresh': True,
    #     '_shards': {'total': 2, 'successful': 1, 'failed': 0},
    #     '_seq_no': 0,
    #     '_primary_term': 1,
    # }

    # search the index
    res_3 = opensearch.search(
        body={
            "size": 5,
            "query": {
                'multi_match': {
                'query': "miller",
                'fields': ['title^2', 'director']
                }
        }}
    )
    print(res_3)
    # {'took': 156,
    #  'timed_out': False,
    #  '_shards': {'total': 3, 'successful': 3, 'skipped': 0, 'failed': 0},
    #  'hits': {'total': {'value': 1, 'relation': 'eq'},
    #   'max_score': 0.2876821,
    #   'hits': [{'_index': 'test-index',
    #     '_type': '_doc',
    #     '_id': '1',
    #     '_score': 0.2876821,
    #     '_source': {'title': 'Moneyball',
    #      'director': 'Bennett Miller',
    #      'year': '2011'}}]}}

    # delete the document
    res_4 = opensearch.delete(
        index="test-index",
        id="1",
    )
    print(res_4)
    # {'_index': 'test-index',
    #     '_type': '_doc',
    #     '_id': '1',
    #     '_version': 2,
    #     'result': 'deleted',
    #     '_shards': {'total': 2, 'successful': 1, 'failed': 0},
    #     '_seq_no': 1,
    #     '_primary_term': 1}

    # delete the index
    res_5 = opensearch.indices.delete(
        index="test-index",
    )
    print(res_5)  # {'acknowledged': True}

```

If you are running a local docker environment, you can clean it up with:

```bash
docker container stop opensearch
docker container rm opensearch
```

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