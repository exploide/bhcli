import subprocess


def test_stats():
    "Test stats subcommand."
    proc = subprocess.run(["bhcli", "stats"], capture_output=True)
    assert proc.returncode == 0
    assert b"User Accounts" in proc.stdout
