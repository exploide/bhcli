import json
import subprocess


def test_cypher():
    """Test cypher subcommand."""
    proc = subprocess.run(["bhcli", "cypher", 'MATCH (u:User) WHERE u.objectid ENDS WITH "-500" RETURN u'], capture_output=True)
    assert proc.returncode == 0
    assert proc.stderr == b""
    result = json.loads(proc.stdout)
    assert len(result["nodes"]) > 0
