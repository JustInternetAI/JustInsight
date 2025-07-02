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
    # "sample-task-every-5-seconds": {
    #     "task": "justinsight.tasks.sample_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    #BUGGY Not fixing right now
    # "check-APfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.apLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    #this feed is WORKING
    # "check-BBCfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.bbcLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    #ALSO BUGGY
    # "check-CBSfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.cbsLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # "check-CNNfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.cnnLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # "check-LATIMESfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.latimesLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # "check-NBCfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.nbcLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # "check-NPRfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.nprLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # "check-NYTfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.nytLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    # "check-USNEWSfeed-every-5-minutes": {
    #     "task": "justinsight.tasks.usnewsLogger_task",
    #     "schedule": 5.0,
    #     "args": (),
    # },

    #schedule more tasks here
}
