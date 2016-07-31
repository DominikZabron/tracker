from celery import Celery

from tracker.settings import REDIS_URL
from tracker.utils import save_item

app = Celery('tasks', broker=REDIS_URL)


@app.task
def db_save(data):
    """Celery task to handle database interactions."""
    save_item(data)
