from ingest.ap_ingestor import APIngestor
from pprint import pprint

def apLogger_task():
    # Create an instance of the class
    ingestor = APIngestor()
    entries = ingestor.check_no_save_new_entries()  #this will not save to a database
    pprint(entries)

if __name__ == '__main__':
    apLogger_task()