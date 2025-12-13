import subprocess


def test_status_api_version():
    "Test status api-version subcommand."
    proc = subprocess.run(["bhcli", "status", "api-version"], capture_output=True)
    assert proc.returncode == 0
    assert b'"server_version": "v' in proc.stdout


def test_status_datapipe():
    "Test status datapipe subcommand."
    proc = subprocess.run(["bhcli", "status", "datapipe"], capture_output=True)
    assert proc.returncode == 0
    assert b'"status": "idle"' in proc.stdout
