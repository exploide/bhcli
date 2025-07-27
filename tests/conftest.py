import configparser
import pathlib
from dataclasses import dataclass

import pytest


@dataclass
class BHCEInstance:
    """The BloodHound CE connection details used for testing."""
    url: str
    username: str
    password: str


@pytest.fixture
def bhce_instance():
    """Create a BHCEInstance object based on a config file."""
    conf = configparser.ConfigParser(allow_unnamed_section=True)
    conf.read(pathlib.Path(__file__).parent / "config.ini")
    section = conf[configparser.UNNAMED_SECTION]
    instance = BHCEInstance(section["url"], section["username"], section["password"])
    return instance
