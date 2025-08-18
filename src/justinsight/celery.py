# celery.py
from celery import Celery

app = Celery(
    "justinsight",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["justinsight.tasks"], 
)

# Optional beat schedule
app.conf.beat_schedule = {
    # Maybe we should just give up on getting AP to work...
    # "check-APfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.apLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # Checked and good 
    "check-BBCfeed-every-5-minutes": {
        "task": "justinsight.tasks.bbcLogger_task",
        "schedule": 5.0,
        "args": (),
    },

    # Checked and good
    # "check-CBSfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.cbsLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # Could not find a current RSS feed for CNN :(
    # "check-CNNfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.cnnLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    #No full-text at all -- only diagnosing issues right now
    # "check-LATIMESfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.latimesLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # Checked and seems good
    # "check-NBCfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.nbcLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # Checked and good 
    # "check-NPRfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.nprLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # Unable to access full text
    # "check-NYTfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.nytLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # Stalls before able ot do anything - I assume an issue with full-text retrieval
    # "check-USNEWSfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.usnewsLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    #schedule more tasks here
}
