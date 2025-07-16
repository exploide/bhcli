import sys

from bhcli.api.exceptions import ApiException
from bhcli.cli import bhcli
from bhcli.logger import log


def main():
    try:
        sys.exit(bhcli())
    except ApiException as e:
        log.error("%s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
