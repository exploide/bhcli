import os
import subprocess
import tempfile
import urllib.request


def test_upload():
    """Test successful upload and ingestion of sample data."""
    url = "https://raw.githubusercontent.com/SpecterOps/BloodHound-Docs/main/docs/assets/sample-data/ad_sampledata.zip"
    with tempfile.TemporaryDirectory() as tmpdir:
        file = os.path.join(tmpdir, "sampledata.zip")
        urllib.request.urlretrieve(url, file)
        proc = subprocess.run(["bhcli", "upload", file], capture_output=True, timeout=180)
    assert proc.returncode == 0
    assert b"Ingestion completed" in proc.stderr
    assert b"WARNING" not in proc.stderr
    assert b"ERROR" not in proc.stderr
