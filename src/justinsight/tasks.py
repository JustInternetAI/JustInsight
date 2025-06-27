from celery import shared_task
from ingest.bbc_ingestor import BBCIngestor
from ingest.cnn_ingestor import CNNIngestor


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
def cnnLogger_task():
    ingestor = CNNIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "CNN RSS Feed checked."

#Add more tasks here in the format of the one above