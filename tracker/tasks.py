import json
from celery import Celery

from tracker.settings import REDIS_URL
from tracker.utils import save_item

app = Celery('tasks', broker=REDIS_URL)


@app.task
def process_request(req_stream, cart_id):
    item_dict = json.loads(req_stream)
    item_dict.update({'cart_id': cart_id})
    save_item(item_dict)
