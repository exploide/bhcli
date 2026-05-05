import subprocess


def test_members():
    "Test members subcommand."
    proc = subprocess.run(["bhcli", "members", "ADMINISTRATORS@PHANTOM.CORP"], capture_output=True)
    assert proc.returncode == 0
    assert b"ADMINISTRATOR@" in proc.stdout


def test_members_nonexistent():
    "Test members subcommand with nonexistent group."
    proc = subprocess.run(["bhcli", "members", "this-does-not-exist"], capture_output=True)
    assert proc.returncode != 0
    assert b"No group found with name" in proc.stderr
