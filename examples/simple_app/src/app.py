import csv
import os
import time
from logging.config import dictConfig

import opensearchpy
from alive_progress import alive_bar
from flask import Flask, request, jsonify
from flask_opensearch import FlaskOpenSearch


# configure logging
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


# initialize app and configure from environment variables
app = Flask(__name__)
app.config["OPENSEARCH_HOST"] = os.environ["OPENSEARCH_HOST"]
app.config["OPENSEARCH_USER"] = os.environ["OPENSEARCH_USER"]
app.config["OPENSEARCH_PASSWORD"] = os.environ["OPENSEARCH_PASSWORD"]


# initialize opensearch extension
opensearch = FlaskOpenSearch(
    app=app,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


@app.route("/healthcheck")
def healthcheck():
    return "healthy"


@app.route("/movies")
def list_movies():
    search = request.args.get("search", "toy story")
    count = int(request.args.get("count", 5))
    count = min(count, 100)
    return jsonify(_search_movies(search, count))


def _search_movies(search, results=5):
    response = opensearch.search(
        body={
            "size": results,
            "query": {"multi_match": {"query": search, "fields": ["title", "original_title", "overview"]}},
        }
    )
    return [x["_source"] for x in response["hits"]["hits"]]


@app.cli.command("load-opensearch")
def load_opensearch():
    print("Load opensearch ...")
    # create index
    print("Creating movies_metadata index")
    try:
        opensearch.indices.create(
            "movies_metadata",
            body={
                "settings": {
                    "index": {
                        "number_of_shards": 1,
                    }
                }
            },
        )
    except opensearchpy.exceptions.RequestError as e:
        print(f"Error creating movies_metadata index: {e}")

    # write data
    print("Inserting documents into movies_metadata index")
    with alive_bar(45466, dual_line=True, title="Loading Movies") as progress_bar:
        progress_bar.text = "Loading movies ..."
        with open("/data/movies_metadata.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    opensearch.index(
                        "movies_metadata",
                        body=row,
                        id=row["id"],
                        refresh=True,
                    )
                except Exception as e:
                    print(f"Error for movie id {row['id']}: {e}")
                time.sleep(0.001)
                progress_bar()


if __name__ == "__main__":
    app.run(debug=True)
