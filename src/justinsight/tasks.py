# tasks.py
from celery import shared_task
from ingest.bbc_ingestor import BBCIngestor


@shared_task
def sample_task():
    print("Sample task!")
    return "done!"

@shared_task
def bbcLogger_task():
    # Create an instance of the class
    ingestor = BBCIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "BBC RSS Feed checked."

@shared_task
def nytLogger_task():
    check_and_save_nyt()
    return "NYT RSS Feed checked."

#Add more tasks here in the format of the one above