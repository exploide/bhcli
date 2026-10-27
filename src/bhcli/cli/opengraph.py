from pathlib import Path

import click

from bhcli.api.exceptions import ApiException
from bhcli.api.from_config import api
from bhcli.logger import log


def import_opengraph_extension_file(filename: Path):
    """Import extension schema from file."""

    if filename.lower().endswith(".json"):
        content_type = "application/json"
    elif filename.lower().endswith(".zip"):
        content_type = "application/zip"
    else:
        log.warning("%s: file of unsupported type will be ignored", filename)
        return
    with open(filename, "rb") as f:
        schema_data = f.read()

    try:
        result = api.import_opengraph_extension(schema_data, content_type)
        if not result:
            log.info("successfully imported %s", filename)
        else:
            log.info("%s: %s", filename, result)
    except ApiException as e:
        if e.response is not None and e.response.status_code == 400:
            log.error(
                "%s: %s",
                filename,
                "\n".join(error["message"] for error in e.response.json()["errors"]),
            )
        else:
            raise


@click.command()
@click.argument("schema", type=click.Path(dir_okay=False), nargs=-1, required=True)
def opengraph(schema):
    """Import OpenGraph extensions.

    Imports an OpenGraph extension schema from a JSON or ZIP file.
    """

    for file in schema:
        import_opengraph_extension_file(file)
