import falcon
import pytest
import uuid

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
    assert 'cart_id' in resp.json


def test_post_item_accept_param(client):
    cart_id = str(uuid.uuid4())
    resp = client.post('/item/{0}'.format(cart_id))
    assert cart_id == resp.json['cart_id']


def test_post_item_handle_cookies(client):
    cart_id = str(uuid.uuid4())
    cookie = 'cart_id={0}'.format(cart_id)
    headers = {'Cookie': cookie}
    resp = client.post('/item', headers=headers)
    assert cart_id == resp.json['cart_id']
    assert cookie == resp.headers['set-cookie'].split(';')[0]
