import os

import pytest
from opensearchpy import OpenSearch

from flask_opensearch import FlaskOpenSearch


def test_pytest_setup():
    assert True


def test_local_docker_opensearch_connection():
    # check that a connection can be made to the local cluster running in docker compose
    host = os.environ.get("OPENSEARCH_HOST", "localhost")
    port = os.environ.get("OPENSEARCH_PORT", 9200)
    auth = ('admin', 'admin')
    opensearch = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )
    assert opensearch.ping() is True


class TestInitApp:
    def test_constructor_calls_init_app_when_app_provided(self, create_app):
        # check that the same connection can be made after initializing the FlaskOpensearch class
        app = create_app()
        with app.app_context():
            opensearch = FlaskOpenSearch(
                app=app,
                use_ssl=True,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
            )
            assert opensearch.ping() is True

            # check some client operations work as expected

    def test_init_app_with_keyword_args(self, create_app):
        app = create_app()
        opensearch = FlaskOpenSearch()
        with app.app_context():
            opensearch.init_app(
                app,
                use_ssl=True,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
            )
            assert opensearch.ping() is True

    def test_constructor_saves_keyword_args(self, create_app):
        app = create_app()
        opensearch = FlaskOpenSearch(
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
        with app.app_context():
            opensearch.init_app(app)
            assert opensearch.ping() is True

    def test_init_app_overwrites_provided_opensearch_options_only(self, create_app):
        app = create_app()
        opensearch = FlaskOpenSearch(
            use_ssl=False,
            verify_certs=False,
        )
        assert opensearch.opensearch_options['use_ssl'] is False
        assert opensearch.opensearch_options['verify_certs'] is False
        with pytest.raises(KeyError):
            opensearch.opensearch_options['ssl_assert_hostname']
        with pytest.raises(KeyError):
            opensearch.opensearch_options['ssl_show_warn']
        with app.app_context():
            opensearch.init_app(
                app,
                use_ssl=True,  # overwrites value provided in constructor
                # uses verify_certs from constructor
                ssl_assert_hostname=False,
                ssl_show_warn=False,
            )
            assert opensearch.opensearch_options['use_ssl'] is True
            assert opensearch.opensearch_options['verify_certs'] is False
            assert opensearch.opensearch_options['ssl_assert_hostname'] is False
            assert opensearch.opensearch_options['ssl_show_warn'] is False

            assert opensearch.ping() is True
# TODO: test against an AWS opensearch instance
