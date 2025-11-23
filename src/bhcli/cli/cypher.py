import json

import click

from bhcli.api.from_config import api


@click.command()
@click.argument("query")
@click.option("--properties/--no-properties", default=True, help="Return (no) node properties (default: yes).")
def cypher(query, properties):
    """Run a raw Cypher query and print the response as JSON."""

    result = api.cypher(query, include_properties=properties)
    print(json.dumps(result, indent=4))
