from mock import MagicMock, patch

from tracker.tasks import db_save

mock = MagicMock()
mock.save_item = MagicMock()


@patch('tracker.tasks.save_item', mock.save_item)
def test_db_save():
    mock.save_item.call_count = 0
    item_dict = {'external_id': 'abc'}
    db_save(item_dict)
    assert mock.save_item.call_count == 1
