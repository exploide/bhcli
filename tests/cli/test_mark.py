import subprocess


def test_mark_owned():
    "Test marking objects as Owned."
    proc = subprocess.run(["bhcli", "mark", "Owned", "ADMINISTRATOR@PHANTOM.CORP", "DC01.PHANTOM.CORP"], capture_output=True)
    assert proc.returncode == 0
    assert b"Marked 2 objects as Owned" in proc.stderr


def test_mark_nonexistent():
    "Test marking a nonexistent object."
    proc = subprocess.run(["bhcli", "mark", "Owned", "this-does-not-exist"], capture_output=True)
    assert b"No Computer object found with name" in proc.stderr
