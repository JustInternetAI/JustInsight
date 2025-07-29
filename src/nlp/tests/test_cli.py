import subprocess
import sys
import pytest

def test_cli_runs_successfully():
    result = subprocess.run(
        [sys.executable, "-m", "nlp.cli", "--article-id", "dummy-id"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Extracted" in result.stdout or "No article" in result.stdout
