# tasks.py
from celery import shared_task
from ingest.bbc_rss import testTask


@shared_task
def sample_task():
    testTask()
    return "done!"