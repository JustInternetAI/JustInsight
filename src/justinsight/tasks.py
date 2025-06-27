from celery import shared_task
from ingest.ap_ingestor import APIngestor
from ingest.bbc_ingestor import BBCIngestor
from ingest.cnn_ingestor import CNNIngestor
from ingest.latimes_ingestor import LATIMESIngestor
from ingest.nbc_ingestor import NBCIngestor
from ingest.npr_ingestor import NPRIngestor
from ingest.nyt_ingestor import NYTIngestor
from ingest.usnews_ingestor import USNEWSIngestor

@shared_task
def sample_task():
    print("Sample task!")
    return "done!"

@shared_task
def apLogger_task():
    # Create an instance of the class
    ingestor = APIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "AP RSS Feed checked."

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

@shared_task
def latimesLogger_task():
    # Create an instance of the class
    ingestor = LATIMESIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "LATIMES RSS Feed checked."

@shared_task
def nbcLogger_task():
    # Create an instance of the class
    ingestor = NBCIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "NBC RSS Feed checked."

@shared_task
def nprLogger_task():
    # Create an instance of the class
    ingestor = NPRIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "NPR RSS Feed checked."

@shared_task
def nytLogger_task():
    # Create an instance of the class
    ingestor = NYTIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "NYT RSS Feed checked."

@shared_task
def usnewsLogger_task():
    # Create an instance of the class
    ingestor = USNEWSIngestor()
    ingestor.check_and_save_new_entries()  # this will invoke the inherited logic
    return "USNEWS RSS Feed checked."

#Add more tasks here in the format of the one above