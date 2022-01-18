import os

import pytest
from flask import Flask


class TestConfig:
    OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST", "localhost")
    OPENSEARCH_USER = os.environ.get("OPENSEARCH_USER", "admin")
    OPENSEARCH_PASSWORD = os.environ.get("OPENSEARCH_PASSWORD", "admin")


class AWSConfig:
    pass


@pytest.fixture
def create_app():
    def _create_app():
        app: Flask = Flask(__name__)
        app.config.from_object(TestConfig)
        return app

    return _create_app
