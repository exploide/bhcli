import subprocess


def test_domains():
    """Test domains subcommand."""
    proc = subprocess.run(["bhcli", "domains", "--collected", "--sid"], capture_output=True)
    assert proc.returncode == 0
    assert b"S-1-5-21" in proc.stdout
