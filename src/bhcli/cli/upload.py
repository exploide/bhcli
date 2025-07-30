import sys
import time
from enum import IntEnum

import click

from bhcli.api.from_config import api
from bhcli.logger import log


class UploadStatus(IntEnum):
    """Status codes for upload jobs."""

    Complete = 2
    Ingesting = 6
    Analyzing = 7


@click.command()
@click.argument("files", metavar="FILE...", nargs=-1, required=True, type=click.Path(exists=True))
def upload(files):
    """Upload and ingest files from the BloodHound collector.

    Supported are JSON and ZIP files.
    """

    log.info("Starting new file upload job...")
    upload_id = api.start_upload()["id"]

    for file in files:
        if file.lower().endswith(".json"):
            content_type = "application/json"
        elif file.lower().endswith(".zip"):
            content_type = "application/zip"
        else:
            log.warning("File of unsupported type will be ignored: %s", file)
            continue
        with open(file, "rb") as f:
            content = f.read()
        log.info("Uploading file %s", file)
        api.upload_file(upload_id, content, content_type)

    log.info("Ending file upload job...")
    api.end_upload(upload_id)

    log.info("Now waiting for ingestion being complete...")
    while True:
        time.sleep(5)
        result = api.upload_status(upload_id)
        if result[0]["status"] in [UploadStatus.Ingesting, UploadStatus.Analyzing]:
            continue
        if result[0]["status"] == UploadStatus.Complete:
            log.info("Ingestion completed, the data is now available.")
            sys.exit(0)
        else:
            log.error("%s", result[0]["status_message"])
            sys.exit(1)
