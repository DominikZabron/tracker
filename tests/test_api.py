import falcon
import pytest

from tracker.urls import app as application
application.req_options.auto_parse_form_urlencoded = True


@pytest.fixture
def app():
    return application


def test_post_item_success(client):
    resp = client.post('/item')
    assert resp.status == falcon.HTTP_201


def test_post_item_returns_correct_response(client):
    resp = client.post('/item')
    assert 'cart_id' in resp.body
