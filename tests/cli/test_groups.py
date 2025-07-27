import subprocess


def test_groups():
    "Test groups subcommand."
    proc = subprocess.run(["bhcli", "groups"], capture_output=True)
    assert proc.returncode == 0
    assert b"ADMINISTRATORS@" in proc.stdout
