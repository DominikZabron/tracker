# -*- coding: utf-8 -*-

import uuid
import pytest
import falcon
import json
from mock import MagicMock, patch

from tracker.utils import cache
from tests.test_utils import db_connection
from tracker.validators import (
    validate_cart_ids_differ,
    validate_cart_id_exists,
    deserialize_request,
    validate_item_values,
)

mock = MagicMock()
mock.exists_0.return_value = 0
mock.exists_1.return_value = 1
mock.cart_id_db_exists_false.return_value = False
mock.cart_id_db_exists_true.return_value = True


def test_validate_cart_ids_equal():
    cart_id = uuid.uuid4()
    validate_cart_ids_differ(cart_id, cart_id)
    assert True


def test_validate_cart_ids_differ():
    cart_id_1 = uuid.uuid4()
    cart_id_2 = uuid.uuid4()
    with pytest.raises(falcon.HTTPBadRequest):
        validate_cart_ids_differ(cart_id_1, cart_id_2)


@patch('tracker.validators.cart_id_db_exists', mock.cart_id_db_exists_true)
@patch('tracker.utils.cache.exists', mock.exists_1)
def test_validate_cart_id_exist_true():
    mock.exists_1.call_count = 0
    mock.cart_id_db_exists_true.call_count = 0
    cart_id = uuid.uuid4()
    validate_cart_id_exists(cart_id, cache, db_connection)
    assert mock.exists_1.call_count == 1
    assert mock.cart_id_db_exists_true.call_count == 0


@patch('tracker.validators.cart_id_db_exists', mock.cart_id_db_exists_false)
@patch('tracker.utils.cache.exists', mock.exists_0)
def test_validate_cart_id_exist_false():
    mock.exists_0.call_count = 0
    mock.cart_id_db_exists_false.call_count = 0
    cart_id = uuid.uuid4()
    with pytest.raises(falcon.HTTPNotFound):
        validate_cart_id_exists(cart_id, cache, db_connection)
    assert mock.exists_0.call_count == 1
    assert mock.cart_id_db_exists_false.call_count == 1


def test_deserialize_request_success():
    payload = {
        'external_id': 'abc'
    }
    deserialize_request(json.dumps(payload))
    assert True


def test_deserialize_request_fail():
    payload = {
        'external_id': 'abc'
    }
    with pytest.raises(falcon.HTTPBadRequest):
        deserialize_request(payload)


def test_validate_item_values_ext_id_is_ascii():
    payload = {
        'external_id': 'abc'
    }
    result = validate_item_values(payload)
    assert type(result) == dict


def test_validate_item_values_ext_id_is_non_ascii():
    payload = {
        'external_id': u'śćżźół'
    }
    with pytest.raises(falcon.HTTPBadRequest):
        validate_item_values(payload)


def test_validate_item_values_no_ext_id():
    payload = {
        'value': 7
    }
    with pytest.raises(falcon.HTTPBadRequest):
        validate_item_values(payload)


def test_validate_item_values_name_is_non_ascii():
    payload = {
        'external_id': 'abc',
        'name': u'śćżźół'
    }
    with pytest.raises(falcon.HTTPBadRequest):
        validate_item_values(payload)


def test_validate_item_values_name_is_ascii():
    payload = {
        'external_id': 'abc',
        'name': 'some_name'
    }
    result = validate_item_values(payload)
    assert type(result) == dict


def test_validate_item_values_value_is_non_int():
    payload = {
        'external_id': 'abc',
        'value': 'five'
    }
    with pytest.raises(falcon.HTTPBadRequest):
        validate_item_values(payload)


def test_validate_item_values_value_is_int():
    payload = {
        'external_id': 'abc',
        'value': 5
    }
    result = validate_item_values(payload)
    assert type(result) == dict


def test_validate_item_values_value_is_int_conv_from_str():
    payload = {
        'external_id': 'abc',
        'value': '5'
    }
    result = validate_item_values(payload)
    assert type(result) == dict


def test_validate_item_values_value_is_int_conv_from_float():
    payload = {
        'external_id': 'abc',
        'value': 5.00000001
    }
    result = validate_item_values(payload)
    assert type(result) == dict
