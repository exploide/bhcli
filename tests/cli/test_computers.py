import subprocess


def test_computers():
    "Test computers subcommand."
    proc = subprocess.run(["bhcli", "computers"], capture_output=True)
    assert proc.returncode == 0
    assert b"DC01." in proc.stdout
