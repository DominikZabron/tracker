import uuid
from mock import MagicMock, patch
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from tracker import settings
from tracker.models import Cart, Item
from tracker.utils import (
    create_cart_id,
    json_loads,
    json_dumps,
    save_item,
)
engine = create_engine(settings.TEST_DB_DSN)
Session = sessionmaker(bind=engine)
session = Session()

mock = MagicMock()
mock.sadd = MagicMock()


def setup_function(function):
    global session


def teardown_function(function):
    session.query(Item).delete()
    session.query(Cart).delete()
    session.commit()
    session.close()


@patch('tracker.utils.cache.sadd', mock.sadd)
def test_create_cart_id():
    mock.cache.call_count = 0
    new_id = create_cart_id()
    assert mock.sadd.call_count == 1
    assert len(new_id) == 36
    assert type(new_id) == str


def test_json_loads():
    raw_json = '{"name": "value"}'
    expect_dict = json_loads(raw_json)
    assert type(expect_dict) == dict


def test_json_dumps():
    dict_obj = {"name": "value"}
    expect_str = json_dumps(dict_obj)
    assert type(expect_str) == str


def test_save_item():
    assert session.query(func.count(Cart.id)).scalar() == 0
    item_dict = {'external_id': 'abc'}
    save_item(item_dict, session=Session)
    assert session.query(func.count(Cart.id)).scalar() == 1
    assert session.query(func.count('*')).select_from(Item).scalar() == 1


def test_save_item_cart_exist():
    cart_id = str(uuid.uuid4())
    session.add(Cart(id=cart_id))
    session.commit()
    assert session.query(func.count(Cart.id)).scalar() == 1
    item_dict = {
        'cart_id': cart_id,
        'external_id': 'xyz',
        'name': 'some name',
        'value': 7
    }
    save_item(item_dict, session=Session)
    assert session.query(func.count(Cart.id)).scalar() == 1
    assert session.query(func.count('*')).select_from(Item).scalar() == 1
    item = session.query(Item).filter(
        Item.cart_id == cart_id,
        Item.external_id == 'xyz',
    ).first()
    assert item.name == 'some name'
    assert item.value == 7


def test_save_item_overwrite_existing():
    cart_id = str(uuid.uuid4())
    session.add(Cart(id=cart_id))
    item = Item(
        cart_id=cart_id,
        external_id='abc',
        name='firstly named',
        value=1
    )
    session.add(item)
    session.commit()

    assert session.query(func.count(Cart.id)).scalar() == 1
    assert session.query(func.count('*')).select_from(Item).scalar() == 1
    assert item.name == 'firstly named'
    assert item.value == 1
    session.close()

    item_dict = {
        'cart_id': cart_id,
        'external_id': 'abc',
        'name': 'secondly named',
        'value': 2
    }
    save_item(item_dict, session=Session)

    assert session.query(func.count(Cart.id)).scalar() == 1
    assert session.query(func.count('*')).select_from(Item).scalar() == 1
    item = session.query(Item).filter(
        Item.cart_id == cart_id,
        Item.external_id == 'abc',
    ).first()
    assert item.name == 'secondly named'
    assert item.value == 2
