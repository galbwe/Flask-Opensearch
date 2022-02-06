from getpass import getpass
from time import sleep

import click
from opensearchpy import OpenSearch


@click.command()
@click.option(
    "-h",
    "--host",
    default="localhost",
    type=str,
    help="The host name of the openesearch cluster. Can be set with OPENSEARCH_HOST environment variable.",
)
@click.option(
    "-p",
    "--port",
    default=9200,
    type=int,
    help="The port opensearch accepts connections on. Can be set with OPENSEARCH_PORT environment variable.",
)
@click.option(
    "-u",
    "--user",
    default="admin",
    type=str,
    help="The opensearch user to authenticate with. Can be set with OPENSEARCH_USER environment variable.",
)
@click.option(
    "-w",
    "--password",
    default="",
    type=str,
    help="The opensearch password to authenticate with. Can be set with OPENSEARCH_PASSWORD environment variable.",
)
@click.option(
    "-n",
    "--number-tries",
    "tries",
    default=5,
    type=int,
    help="The maximum number of times to retry connecting to the opensearch cluster.",
)
@click.option("-s", "--seconds", default=5, type=int, help="The time in seconds between connection attempts.")
@click.option("-y", "--skip-prompts", "skip_prompts", is_flag=True, help="Skip password prompts.")
def wait_for_opensearch(host, port, user, password, tries, seconds, skip_prompts):

    if not password and not skip_prompts:
        password = getpass()

    t = 0
    ready = False

    auth = (user, password)
    opensearch = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    while t < tries and not ready:
        t += 1
        click.echo("Pinging OpenSearch cluster ...")
        ready = opensearch.ping()
        if not ready:
            sleep(seconds)

    assert t < tries, "Could not connect to OpenSearch cluster. Abort!"

    click.echo("OpenSearch is ready!")


if __name__ == "__main__":
    wait_for_opensearch(auto_envvar_prefix="OPENSEARCH")
