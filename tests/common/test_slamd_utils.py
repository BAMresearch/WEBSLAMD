from slamd.common.slamd_utils import empty, not_empty, join_all


def test_empty_returns_true_when_input_is_none():
    assert empty(None) is True


def test_empty_returns_true_when_input_is_empty():
    assert empty('') is True


def test_empty_returns_false_when_input_is_not_empty():
    assert empty('some input string') is False


def test_not_empty_returns_false_when_input_is_none():
    assert not_empty(None) is False


def test_not_empty_returns_false_when_input_is_empty():
    assert not_empty('') is False


def test_not_empty_returns_true_when_input_is_not_empty():
    assert not_empty('some input string') is True


def test_join_all_creates_empty_string_when_none_is_passed():
    assert join_all(None) == ''


def test_join_all_creates_empty_string_when_empty_list_is_passed():
    assert join_all([]) == ''


def test_join_all_creates_string_when_list_with_single_item_is_passed():
    assert join_all(['some item']) == 'some item'


def test_join_all_create_string_when_list_with_multiple_items_is_passed():
    assert join_all(['item 1', 'item 2']) == 'item 1item 2'
