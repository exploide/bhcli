import subprocess


def test_clear_db():
    "Test clear-db subcommand."
    proc = subprocess.run(["bhcli", "clear-db", "--all"], capture_output=True)
    assert proc.returncode == 0
    assert b"Data deletion started" in proc.stderr
