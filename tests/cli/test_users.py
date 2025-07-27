import subprocess


def test_users():
    "Test users subcommand."
    proc = subprocess.run(["bhcli", "users"], capture_output=True)
    assert proc.returncode == 0
    assert b"ADMINISTRATOR@" in proc.stdout
