import subprocess


def test_audit():
    "Test audit subcommand."
    proc = subprocess.run(["bhcli", "audit"], capture_output=True)
    assert proc.returncode == 0
    assert b"Kerberoastable user accounts" in proc.stdout
