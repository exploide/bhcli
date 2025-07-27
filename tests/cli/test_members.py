import subprocess


def test_members():
    "Test members subcommand."
    proc = subprocess.run(["bhcli", "members", "ADMINISTRATORS@PHANTOM.CORP"], capture_output=True)
    assert proc.returncode == 0
    assert b"ADMINISTRATOR@" in proc.stdout
