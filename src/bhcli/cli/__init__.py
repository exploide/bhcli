import click

from bhcli.__about__ import __version__
from bhcli import logger
from .audit import audit
from .auth import auth
from .clear_db import clear_db
from .computers import computers
from .cypher import cypher
from .domains import domains
from .groups import groups
from .mark import mark
from .members import members
from .queries import queries
from .stats import stats
from .status import status
from .upload import upload
from .users import users


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--debug", is_flag=True, help="Enable debug output.")
@click.version_option(version=__version__, prog_name="bhcli")
def bhcli(debug=False):
    """CLI tool to interact with the BloodHound CE API"""

    logger.set_loglevel(debug)


bhcli.add_command(audit)
bhcli.add_command(auth)
bhcli.add_command(clear_db)
bhcli.add_command(computers)
bhcli.add_command(cypher)
bhcli.add_command(domains)
bhcli.add_command(groups)
bhcli.add_command(mark)
bhcli.add_command(members)
bhcli.add_command(queries)
bhcli.add_command(stats)
bhcli.add_command(status)
bhcli.add_command(upload)
bhcli.add_command(users)
