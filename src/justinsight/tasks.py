# tasks.py
from celery import shared_task
from ingest.bbc_rss import check_and_save_new_entries as check_and_save_bbc
from ingest.nyt_rss import check_and_save_new_entries as check_and_save_nyt


@shared_task
def sample_task():
    print("Sample task!")
    return "done!"

@shared_task
def bbcLogger_task():
    check_and_save_bbc()
    return "BBC RSS Feed checked."

@shared_task
def nytLogger_task():
    check_and_save_nyt()
    return "NYT RSS Feed checked."

#Add more tasks here in the format of the one above