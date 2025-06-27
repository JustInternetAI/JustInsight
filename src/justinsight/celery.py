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

    "check-BBCfeed-every-5-minutes": {
        "task": "justinsight.tasks.bbcLogger_task",
        "schedule": 5.0,
        "args": (),
    },

    "check-CNNfeed-every-5-minutes": {
        "task": "justinsight.tasks.cnnLogger_task",
        "schedule": 5.0,
        "args": (),
    },

    #schedule more tasks here
}
