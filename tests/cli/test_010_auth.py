import os
import shutil
import subprocess


def remove_config_dir():
    """Remove bhcli config directory."""
    config_home = os.environ.get("XDG_CONFIG_HOME", default=os.path.join(os.path.expanduser("~"), ".config"))
    config_dir = os.path.join(config_home, "bhcli")
    shutil.rmtree(config_dir, ignore_errors=True)


def test_auth_invalid_url(bhce_instance):
    """Test connection failure with invalid URL."""
    remove_config_dir()
    proc = subprocess.run(["bhcli", "auth", "-u", "irrelevant-user", "-p", "invalid-password", "http://127.0.0.1:5"], capture_output=True)
    assert proc.returncode > 0
    assert b"Could not connect to API server" in proc.stderr


def test_auth_invalid_creds(bhce_instance):
    """Test authentication failure with invalid password."""
    remove_config_dir()
    proc = subprocess.run(["bhcli", "auth", "-u", bhce_instance.username, "-p", "invalid-password", bhce_instance.url], capture_output=True)
    assert proc.returncode > 0
    assert b"Authentication failure" in proc.stderr


def test_auth_valid_creds(bhce_instance):
    """Test successful authentication."""
    remove_config_dir()
    proc = subprocess.run(["bhcli", "auth", "-u", bhce_instance.username, "-p", bhce_instance.password, bhce_instance.url], capture_output=True)
    assert proc.returncode == 0
    assert b"bhcli is now configured" in proc.stderr
