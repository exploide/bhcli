import subprocess


def test_mark_owned():
    "Test marking objects as owned."
    proc = subprocess.run(["bhcli", "mark", "owned", "ADMINISTRATOR@PHANTOM.CORP", "DC01.PHANTOM.CORP"], capture_output=True)
    assert proc.returncode == 0
    assert b"Marked 2 objects as owned" in proc.stderr


def test_mark_custom_asset_group():
    "Test marking objects as belonging to a custom asset group."
    proc = subprocess.run(["bhcli", "mark", "--create-asset-group", "Custom", "custom", "GUEST@PHANTOM.CORP"], capture_output=True)
    assert proc.returncode == 0
    assert b"Marked 1 objects as custom" in proc.stderr
