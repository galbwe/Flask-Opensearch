import csv
import os
import time
from logging.config import dictConfig

import opensearchpy
from alive_progress import alive_bar
from flask import Flask, request, jsonify, render_template
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
        "root": {"level": os.environ.get("LOG_LEVEL", "INFO").upper(), "handlers": ["wsgi"]},
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


@app.route("/movies", methods=["GET", "POST"])
def movies():
    if request.method == "POST":
        search = request.form["search"]
        count = int(request.form["count"])
    else:
        search = "avatar"
        count = 5

    query = {
        "search": search,
        "count": count,
    }
    movies = _search_movies(search, count)

    app.logger.info(f"query: {query}")
    app.logger.info(f"movies: {movies}")
    return render_template("movies.html", movies=movies, query=query)


@app.route("/api/movies")
def list_movies():
    search = request.args.get("search", "toy story")
    count = int(request.args.get("count", 5))
    count = min(count, 100)
    return jsonify(_search_movies(search, count))


API_DATA_MODEL = {
    "adult": bool,
    "belongs_to_collection": eval,
    "budget": int,
    "genres": eval,
    "homepage": str,
    "id": int,
    "imdb_id": str,
    "original_language": str,
    "overview": str,
    "popularity": float,
    "poster_path": str,
    "production_companies": eval,
    "production_countries": eval,
    "release_date": str,
    "revenue": int,
    "runtime": float,
    "spoken_languages": eval,
    "status": str,
    "tagline": str,
    "title": str,
    "video": bool,
    "vote_average": float,
    "vote_count": int,
}


def _search_movies(search, count=5):
    response = opensearch.search(
        body={
            "size": count,
            "query": {"multi_match": {"query": search, "fields": ["title", "original_title", "overview"]}},
        }
    )

    movies = []

    hits = response["hits"]["hits"]
    for hit in hits:
        source = hit.get("_source")
        if source is None:
            app.logger.error(f"Unexpected json shape from opensource\n hit: {hit}.")
            continue

        movie = {}
        missing_fields = []
        for field, parse in API_DATA_MODEL.items():
            value = source.get(field)
            if value is not None:
                try:
                    movie[field] = parse(value)
                except Exception as e:
                    movie[field] = None
                    app.logger.error(
                        f"Failed to parse field:\n field: {field}\n value: {source[field]}\n parser: {parse}"
                    )
                    app.logger.error(e)
            else:
                movie[field] = None
                missing_fields.append(field)

            if missing_fields:
                app.logger.error(f"Missing fields {', '.join(missing_fields)} in opensearch response\n hit: {hit}")
                app.logger.error(f"hit: {hit}")

            movies.append(movie)

    return movies

    # deserialize json string fields

    return [x["_source"] for x in response["hits"]["hits"]]


@app.cli.command("load-opensearch")
def load_opensearch():
    MOVIE_COUNT = 45466
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
    with alive_bar(MOVIE_COUNT, dual_line=True, title="Loading Movies") as progress_bar:
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
