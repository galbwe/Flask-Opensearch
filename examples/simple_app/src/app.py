import csv
import os
import time

from alive_progress import alive_bar
from flask import Flask
from flask_opensearch import FlaskOpenSearch



app = Flask(__name__)

app.config["OPENSEARCH_HOST"] = os.environ["OPENSEARCH_HOST"]
app.config["OPENSEARCH_USER"] = os.environ["OPENSEARCH_USER"]
app.config["OPENSEARCH_PASSWORD"] = os.environ["OPENSEARCH_PASSWORD"]

opensearch = FlaskOpenSearch(
    app=app,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.cli.command("load-opensearch")
def load_opensearch():
    print("Load opensearch ...")
    # create index
    print("Creating movies_metadata index")
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
