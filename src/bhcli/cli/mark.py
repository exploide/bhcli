import sys

import click

from bhcli.api.from_config import api
from bhcli.logger import log
from .paramtypes import AssetGroupTagType


@click.command()
@click.argument("tag", type=AssetGroupTagType())
@click.argument("objects", metavar="[OBJECT]...", nargs=-1)
@click.option("--file", "-f", type=click.Path(exists=True, dir_okay=False, allow_dash=True), help="File containing object names to mark (use '-' for stdin).")
def mark(tag, objects, file):
    """Mark objects with an asset group tag (Owned, Tier Zero).

    The first argument is the asset group tag the objects should be added to (e.g. 'Owned' or 'Tier Zero').

    The full BloodHound label must be given as the object name.
    Only User and Computer objects are supported for now.
    If the name contains an '@', it is treated as a User, otherwise as a Computer.
    """

    asset_group_tags = api.get_asset_group_tags(name=tag)
    if len(asset_group_tags) == 0:
        log.error("Asset group tag '%s' not found!", tag)
        sys.exit(1)
    asset_group_tag_id = asset_group_tags[0]["id"]

    asset_group_tag_members = api.get_asset_group_tag_members(asset_group_tag_id)
    sids_already_tagged = set(member["object_id"] for member in asset_group_tag_members)

    names_to_add = list(objects)

    if file:
        with click.open_file(file, mode="r", encoding="UTF-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    names_to_add.append(line)

    sids_to_add = set()

    for obj in names_to_add:
        if "@" in obj:
            kind = "User"
        else:
            kind = "Computer"
        result = api.search(obj, kind)
        result = [x for x in result if x["name"].upper() == obj.upper()]
        if len(result) < 1:
            log.warning("No %s object found with name: %s", kind, obj)
            continue
        if len(result) > 1:
            log.warning("This should not happen! Found more than one %s object with name: %s", kind, obj)
            continue
        result = result[0]
        if result["objectid"] in sids_already_tagged:
            log.warning("%s object is already marked as %s: %s", kind, tag, result["name"])
            continue
        sids_to_add.add(result["objectid"])

    if sids_to_add:
        api.add_to_asset_group_tag(asset_group_tag_id, list(sids_to_add))
        log.info("Marked %d objects as %s.", len(sids_to_add), tag)
