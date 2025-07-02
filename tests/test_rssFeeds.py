from ingest.ap_ingestor import APIngestor

def apLogger_task():
    # Create an instance of the class
    ingestor = APIngestor()
    ingestor.check_and_save_new_entries(using_celery=True)  # this will invoke the inherited logic
    print("AP RSS Feed checked.")


if __name__ == '__main__':
    apLogger_task()