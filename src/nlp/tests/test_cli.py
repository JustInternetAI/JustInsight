from unittest.mock import patch
from nlp.cli import run_cli

def test_run_cli_prints_extracted_message(capfd):
    with patch("nlp.cli.process_article", return_value=[{"entity_group": "PER"}]):
        run_cli("dummy-id")
        out, _ = capfd.readouterr()
        assert "Extracted 1 entities" in out

