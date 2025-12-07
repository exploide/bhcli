import sys

import click

from bhcli.api.from_config import api
from bhcli.logger import log


@click.command()
@click.option("--all", "all_data", is_flag=True, default=False, help="Delete all data.")
@click.option("--graph-data/--keep-graph-data", default=None, help="Delete or keep graph data of any kind.")
@click.option("--ad-graph-data/--keep-ad-graph-data", default=None, help="Delete or keep Active Directory graph data.")
@click.option("--azure-graph-data/--keep-azure-graph-data", default=None, help="Delete or keep Azure graph data.")
@click.option("--sourceless-graph-data/--keep-sourceless-graph-data", default=None, help="Delete or keep sourceless graph data.")
@click.option("--asset-group-selectors/--keep-asset-group-selectors", default=None, help="Delete or keep asset group selectors.")
@click.option("--file-ingest-history/--keep-file-ingest-history", default=None, help="Delete or keep file ingest log history.")
@click.option("--data-quality-history/--keep-data-quality-history", default=None, help="Delete or keep data quality history.")
def clear_db(all_data, graph_data, ad_graph_data, azure_graph_data, sourceless_graph_data, asset_group_selectors, file_ingest_history, data_quality_history):
    """Delete data from the database.

    \b
    Different data can be deleted or explicitly kept.
    --all deletes everything unless explicitly kept.
    --graph-data deletes AD, Azure and sourceless graph data unless explicitly kept.
    """

    if not any((all_data, graph_data, ad_graph_data, azure_graph_data, sourceless_graph_data, asset_group_selectors, file_ingest_history, data_quality_history)):
        log.error("Nothing selected for deletion. Specify any option.")
        sys.exit(1)

    api.clear_database(all_data, graph_data, ad_graph_data, azure_graph_data, sourceless_graph_data, asset_group_selectors, file_ingest_history, data_quality_history)

    log.info("Data deletion started. This may take some time to complete.")
