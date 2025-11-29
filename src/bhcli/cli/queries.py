import io
import json
import os
import sys
import zipfile

import click

from bhcli.api.exceptions import ApiException
from bhcli.api.from_config import api
from bhcli.logger import log


def export_queries_to_single_json(outfile):
    """Export queries to single JSON file containing all queries."""

    result = api.get_saved_queries(sort_by="name")
    queries_to_export = [
        {
            key: entry[key] for key in ("name", "query", "description")
        }
        for entry in result
    ]
    with open(outfile, "w", encoding="UTF-8") as f:
        json.dump(queries_to_export, f, indent=4)
    log.info("Saved %d queries to %s", len(queries_to_export), outfile)


def export_queries_to_zip(outfile):
    """Export queries to ZIP file containing one JSON file per query."""

    result = api.export_saved_queries()
    with open(outfile, "wb") as f:
        f.write(result)
    log.info("Saved all queries to %s", outfile)


def export_queries_to_jsons_in_dir(directory):
    """Export queries to directory, one JSON file per query."""

    result = api.export_saved_queries()
    with zipfile.ZipFile(io.BytesIO(result), "r") as f:
        f.extractall(directory)
        log.info("Saved %d queries to %s", len(f.namelist()), directory)


def import_queries_from_zip(filename):
    """Import queries from ZIP file containing one JSON file per query."""

    with open(filename, "rb") as f:
        zipdata = f.read()
    try:
        result = api.import_saved_queries(zipdata, "application/zip")
        log.info("%s: %s", filename, result)
    except ApiException as e:
        if e.response is not None and e.response.status_code == 400:
            log.error(
                "%s: %s",
                filename,
                '\n'.join(error["message"] for error in e.response.json()["errors"]),
            )
        else:
            raise


def import_queries_from_json(filename):
    """Import queries from JSON file (various formats)."""

    try:
        with open(filename, "r", encoding="UTF-8") as f:
            jsondata = json.load(f)
    except (json.decoder.JSONDecodeError, UnicodeDecodeError) as e:
        log.error("%s: cannot parse JSON: %s", filename, e)
        return 0

    if isinstance(jsondata, dict) and "queries" in jsondata:
        log.warning("%s: Detected legacy BloodHound's customqueries.json format. Some queries might not be compatible with BloodHound CE.", filename)
        queries_to_import = parse_legacy_json(jsondata)
    elif isinstance(jsondata, list):
        # multiple queries in one JSON file
        queries_to_import = jsondata
    else:
        # one query in JSON file
        queries_to_import = [jsondata]

    num_queries = 0
    for query in queries_to_import:
        try:
            api.add_saved_query(
                query["name"],
                query["query"],
                query.get("description", ""),
            )
            num_queries += 1
        except KeyError as e:
            log.error("%s: Query with invalid input format, missing key %s. Skipping...", filename, e)
            continue
        except ApiException as e:
            if e.response is not None and e.response.status_code == 400:
                log.error(
                    "%s: %s: %s",
                    filename,
                    query["name"],
                    '\n'.join(error["message"] for error in e.response.json()["errors"]),
                )
            else:
                raise
    return num_queries


def parse_legacy_json(jsondata):
    """Parse legacy BloodHound's customqueries.json format."""

    queries_to_import = []
    for entry in jsondata["queries"]:
        if len(entry["queryList"]) > 1 or not entry["queryList"][0]["final"]:
            log.error('Query "%s" requires node selection, which is not compatible with BloodHound CE. Skipping...', entry["name"])
            continue
        queries_to_import.append(
            {
                "name": entry["name"],
                "query": entry["queryList"][0]["query"],
            }
        )
    return queries_to_import


def import_queries_from_dir(directory):
    """Import queries from directory containing JSON files."""

    num_queries = 0
    for file in os.listdir(directory):
        if file.lower().endswith(".json"):
            num_queries += import_queries_from_json(os.path.join(directory, file))
    return num_queries


@click.command()
@click.argument("files", type=click.Path(dir_okay=True), nargs=-1, required=True)
@click.option("--save", is_flag=True, help="Export existing custom queries.")
def queries(files, save):
    """Import and export custom queries.

    Imports custom Cypher queries from files to the BloodHound database.
    A file must either be in a format that --save produces or in the legacy Bloodhound's customqueries.json format.
    However, not everything from the latter might be compatible.

    \b
    If --save is specified, existing queries are exported instead of imported.
    The output format depends on the specified output file:
      - file.json: single JSON file containing all queries
      - file.zip: ZIP file containing one JSON file per query
      - directory: one JSON file per query stored in directory
    """

    if save:
        # export queries
        if len(files) != 1:
            log.error("Exactly one argument is required when exporting.")
            sys.exit(1)
        outfile = files[0]
        if outfile.lower().endswith(".json"):
            export_queries_to_single_json(outfile)
        elif outfile.lower().endswith(".zip"):
            export_queries_to_zip(outfile)
        elif os.path.isdir(outfile):
            export_queries_to_jsons_in_dir(outfile)
        else:
            log.error("Unexpected output file with unknown format.")
            sys.exit(1)

    else:
        # import queries
        for file in files:
            if file.lower().endswith(".json"):
                num_queries = import_queries_from_json(file)
                log.info("%s: imported %d queries", file, num_queries)
            elif file.lower().endswith(".zip"):
                import_queries_from_zip(file)
            elif os.path.isdir(file):
                num_queries = import_queries_from_dir(file)
                log.info("%s: imported %d queries", file, num_queries)
            else:
                log.error("Unexpected input file with unknown format.")
