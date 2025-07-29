import pytest
from unittest.mock import patch
from nlp.tasks import ner_task

@patch("nlp.core.process_article")
def test_ner_task_calls_process_article(mock_process_article):
    mock_process_article.return_value = [{"entity": "PERSON", "word": "Alice"}]

    result = ner_task("dummy_article_id")
    mock_process_article.assert_called_once_with("dummy_article_id")
    assert result == mock_process_article.return_value
