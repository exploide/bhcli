import json
import os
import subprocess
import tempfile


test_queries = [
    {
        'name': 'test_query_1',
        'query': 'MATCH (u:User) WHERE u.objectid ENDS WITH "-500" RETURN u',
        'irrelevant-key': 'this dict key should be silently ignored',
    }
]


def test_queries_import():
    """Test importing custom queries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file = os.path.join(tmpdir, "queries_import.json")
        with open(file, "w") as f:
            json.dump(test_queries, f)
        proc = subprocess.run(["bhcli", "queries", file], capture_output=True)
    assert proc.returncode == 0
    assert b"imported 1 queries" in proc.stderr
    assert b"ERROR" not in proc.stderr


def test_queries_export():
    """Test exporting custom queries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file = os.path.join(tmpdir, "queries_export.json")
        proc = subprocess.run(["bhcli", "queries", "--save", file], capture_output=True)
        assert proc.returncode == 0
        with open(file, "r") as f:
            queries = json.load(f)
    assert test_queries[0]["name"] in [query["name"] for query in queries]
    assert test_queries[0]["query"] in [query["query"] for query in queries]
