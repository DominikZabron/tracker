from tracker.tasks import process_request


def queue_request(req, resp, resource):
    process_request.delay(req.stream.read(), resource.cart_id)
    # process_request.delay(None, None)
