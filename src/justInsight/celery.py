# celery.py
from celery import Celery

app = Celery(
    "justInsight",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["justInsight.tasks"],  # adjust this to your tasks file
)

# Optional beat schedule
app.conf.beat_schedule = {
    "sample-task-every-10-seconds": {
        "task": "justInsight.tasks.sample_task",
        "schedule": 10.0,
        "args": (),
    },
}
