import os

from flask import Flask

from flask_opensearch import FlaskOpenSearch


def test_readme_example():

    # create a flask app
    app = Flask(__name__)

    # add opensearch configuration to the app
    app.config["OPENSEARCH_HOST"] = os.environ["OPENSEARCH_HOST"]
    app.config["OPENSEARCH_USER"] = os.environ["OPENSEARCH_USER"]
    app.config["OPENSEARCH_PASSWORD"] = os.environ["OPENSEARCH_PASSWORD"]
    with app.app_context():
        # instantiate the FlaskOpenSearch class
        opensearch = FlaskOpenSearch(
            app=app,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
        # check that the connection is working
        assert opensearch.ping() is True
        # create an index
        res_1 = opensearch.indices.create(
            "test-index",
            body={
                "settings": {
                    "index": {
                        "number_of_shards": 1,
                    }
                }
            },
        )
        assert res_1 == {"acknowledged": True, "shards_acknowledged": True, "index": "test-index"}

        # add a document to the index
        res_2 = opensearch.index(
            "test-index",
            body={"title": "Moneyball", "director": "Bennett Miller", "year": "2011"},
            id="1",
            refresh=True,
        )
        assert res_2 == {
            "_index": "test-index",
            "_type": "_doc",
            "_id": "1",
            "_version": 1,
            "result": "created",
            "forced_refresh": True,
            "_shards": {"total": 2, "successful": 1, "failed": 0},
            "_seq_no": 0,
            "_primary_term": 1,
        }

        # search the index
        res_3 = opensearch.search(
            body={"size": 5, "query": {"multi_match": {"query": "miller", "fields": ["title^2", "director"]}}}
        )
        assert res_3 == {
            "took": 156,
            "timed_out": False,
            "_shards": {"total": 3, "successful": 3, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 1, "relation": "eq"},
                "max_score": 0.2876821,
                "hits": [
                    {
                        "_index": "test-index",
                        "_type": "_doc",
                        "_id": "1",
                        "_score": 0.2876821,
                        "_source": {"title": "Moneyball", "director": "Bennett Miller", "year": "2011"},
                    }
                ],
            },
        }

        # delete the document
        res_4 = opensearch.delete(
            index="test-index",
            id="1",
        )
        assert res_4 == {
            "_index": "test-index",
            "_type": "_doc",
            "_id": "1",
            "_version": 2,
            "result": "deleted",
            "_shards": {"total": 2, "successful": 1, "failed": 0},
            "_seq_no": 1,
            "_primary_term": 1,
        }

        # delete the index
        res_5 = opensearch.indices.delete(
            index="test-index",
        )
        assert res_5 == {"acknowledged": True}
