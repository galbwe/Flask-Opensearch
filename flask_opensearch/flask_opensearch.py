from opensearchpy import OpenSearch


# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


# TODO: switch to current_app instead of self.app to support multiple applications running in the same process
# TODO: instantiate AWSRequestsAuth if OPENSEARCH_HTTP_AUTH is not set


class FlaskOpenSearch:
    def __init__(self, app=None, **kwargs):
        self.app = app
        self.opensearch_options = kwargs
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        host = app.config.get("OPENSEARCH_HOST", "localhost")
        port = app.config.setdefault("OPENSEARCH_PORT", 9200)
        app.config.setdefault("OPENSEARCH_HOST_OBJECTS", [{"host": host, "port": port}])
        user = app.config.get("OPENSEARCH_USERNAME", "admin")
        password = app.config.get("OPENSEARCH_PASSWORD", "admin")
        http_auth = (user, password)
        app.config.setdefault("OPENSEARCH_HTTP_AUTH", http_auth)

        for (key, value) in kwargs.items():
            self.opensearch_options[key] = value

        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, "teardown_appcontext"):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def __getattr__(self, item):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, "opensearch"):
                hosts = ctx.app.config.get("OPENSEARCH_HOST_OBJECTS")
                ctx.opensearch = OpenSearch(
                    hosts=hosts, http_auth=ctx.app.config.get("OPENSEARCH_HTTP_AUTH"), **self.opensearch_options
                )

            return getattr(ctx.opensearch, item)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, "opensearch"):
            ctx.opensearch = None
