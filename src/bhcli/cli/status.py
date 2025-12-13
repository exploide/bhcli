import json

import click

from bhcli.api.from_config import api


@click.command()
@click.argument("item", type=click.Choice(("api-version", "datapipe")))
def status(item):
    """Retrieve internal status of the BloodHound server.

    \b
    The argument must be one of the following properties:
    api-version -- print version info for API and server
    datapipe -- print current status of the datapipe
    """

    data = {}

    if item == "api-version":
        data = api.api_version()

    if item == "datapipe":
        data = api.datapipe_status()

    print(json.dumps(data, indent=4))
