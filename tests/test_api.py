import falcon
import pytest
import uuid
from mock import patch, MagicMock

from tracker.urls import app as application

application.req_options.auto_parse_form_urlencoded = True

mock = MagicMock()
mock.sismember.return_value = 1
mock.sadd = MagicMock()
mock.proc_req_delay = MagicMock()


@pytest.fixture
def app():
    return application


@patch('tracker.hooks.process_request.delay', mock.proc_req_delay)
@patch('tracker.utils.cache.sadd', mock.sadd)
def test_post_item_success(client):
    mock.sadd.call_count = 0
    resp = client.post('/item')
    assert resp.status == falcon.HTTP_201
    assert mock.sadd.call_count == 1


@patch('tracker.hooks.process_request.delay', mock.proc_req_delay)
@patch('tracker.utils.cache.sadd', mock.sadd)
def test_post_item_returns_correct_response(client):
    mock.sadd.call_count = 0
    resp = client.post('/item')
    assert 'cart_id' in resp.json
    assert mock.sadd.call_count == 1


@patch('tracker.hooks.process_request.delay', mock.proc_req_delay)
@patch('tracker.validators.cache.sismember', mock.sismember)
def test_post_item_accept_param(client):
    mock.sismember.call_count = 0
    cart_id = str(uuid.uuid4())
    resp = client.post('/item/{0}'.format(cart_id))
    assert cart_id == resp.json['cart_id']
    assert mock.sismember.call_count == 1


@patch('tracker.hooks.process_request.delay', mock.proc_req_delay)
@patch('tracker.validators.cache.sismember', mock.sismember)
def test_post_item_handle_cookies(client):
    mock.sismember.call_count = 0
    cart_id = str(uuid.uuid4())
    cookie = 'cart_id={0}'.format(cart_id)
    headers = {'Cookie': cookie}
    resp = client.post('/item', headers=headers)
    assert cart_id == resp.json['cart_id']
    assert cookie == resp.headers['set-cookie'].split(';')[0]
    assert mock.sismember.call_count == 1


@patch('tracker.hooks.process_request.delay', mock.proc_req_delay)
@patch('tracker.validators.cache.sismember', mock.sismember)
def test_post_item_validate_input_fail(client):
    mock.sismember.call_count = 0
    uuid_1, uuid_2 = str(uuid.uuid4()), str(uuid.uuid4())
    cookie = 'cart_id={0}'.format(uuid_1)
    headers = {'Cookie': cookie}
    resp = client.post('/item/{0}'.format(uuid_2), headers=headers)
    assert resp.status == falcon.HTTP_400
    assert resp.json['title'] == "Bad request"
    assert mock.sismember.call_count == 0


@patch('tracker.hooks.process_request.delay', mock.proc_req_delay)
@patch('tracker.validators.cache.sismember', mock.sismember)
def test_post_item_validate_input_success(client):
    mock.sismember.call_count = 0
    cart_id = str(uuid.uuid4())
    cookie = 'cart_id={0}'.format(cart_id)
    headers = {'Cookie': cookie}
    resp = client.post('/item/{0}'.format(cart_id), headers=headers)
    assert resp.status == falcon.HTTP_201
    assert mock.sismember.call_count == 1


@patch('tracker.hooks.process_request.delay', mock.proc_req_delay)
@patch('tracker.utils.cache.sadd', mock.sadd)
def test_post_item_cart_id_not_exist(client):
    mock.sadd.call_count = 0
    cart_id = str(uuid.uuid4())
    resp = client.post('/item/{0}'.format(cart_id))
    assert resp.status == falcon.HTTP_404
    assert mock.sadd.call_count == 0
