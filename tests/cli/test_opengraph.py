import json
import subprocess
import tempfile

SCHEMA_JSON = {
    "schema": {
        "name": "TEST",
        "display_name": "TEST Extension",
        "version": "v0.0.1",
        "namespace": "TEST",
    },
    "node_kinds": [
        {
            "name": "TEST_Node",
            "display_name": "test node",
            "description": "test node",
            "is_display_kind": True,
            "icon": "building-circle-arrow-right",
            "color": "#FFFFFF",
        }
    ],
    "relationship_kinds": [
        {"name": "TEST_edge", "description": "test edge", "is_traversable": True}
    ],
    "environments": [],
    "relationship_findings": [],
}


def test_upload_opengraph_extension_json():
    "Test uploading an opengraph extension."
    with tempfile.NamedTemporaryFile("w") as f:
        json.dump(SCHEMA_JSON, f)
        f.flush()

        proc = subprocess.run(
            ["bhcli", "opengraph", f.name, f.name],
        )
    assert proc.returncode == 0
