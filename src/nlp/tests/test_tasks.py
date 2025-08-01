from unittest.mock import patch

@patch("nlp.core.process_article")
@patch("ingest.save_to_database.collection")
def test_ner_task_calls_process_article(mock_collection, mock_process_article):
    # Mock the DB find_one call
    mock_collection.find_one.return_value = {
        "id": "dummy_article_id",
        "full_text": "Some article text",
        "processed": False
    }
    
    mock_process_article.return_value = [{"entity": "PERSON", "word": "Alice"}]
    
    from nlp.tasks import ner_task
    result = ner_task("dummy_article_id")
    
    mock_process_article.assert_called_once_with("dummy_article_id")
    assert result == [{"entity": "PERSON", "word": "Alice"}]