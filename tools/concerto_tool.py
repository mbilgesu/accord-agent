"""
tools/concerto_tool.py
======================
Wrapper around the Accord Project concerto CLI.
Agents call this to validate generated Concerto models.
"""

import subprocess
import tempfile
import os
from pathlib import Path


def validate_concerto_model(model_content: str) -> dict:
    """
    Write model_content to a temp .cto file and run:
        concerto validate --model <file>
    Returns {"valid": bool, "output": str, "errors": str}
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".cto", delete=False
    ) as tmp:
        tmp.write(model_content)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["concerto", "validate", "--model", tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "valid": result.returncode == 0,
            "output": result.stdout.strip(),
            "errors": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"valid": False, "output": "", "errors": "concerto CLI timed out"}
    except FileNotFoundError:
        return {"valid": False, "output": "", "errors": "concerto CLI not found"}
    finally:
        os.unlink(tmp_path)


def validate_model_file(path: str) -> dict:
    """Validate an existing .cto file by path."""
    result = subprocess.run(
        ["concerto", "validate", "--model", path],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "valid": result.returncode == 0,
        "output": result.stdout.strip(),
        "errors": result.stderr.strip(),
    }