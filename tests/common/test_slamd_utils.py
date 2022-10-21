from slamd.common.slamd_utils import empty, not_empty, join_all, not_numeric, float_if_not_empty, str_if_not_none


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


def test_float_if_not_empty_returns_none_for_empty_string():
    assert float_if_not_empty('') == None


def test_float_if_not_empty_returns_none_for_none():
    assert float_if_not_empty(None) == None


def test_float_if_not_empty_returns_float_for_string_with_number():
    assert float_if_not_empty('1234.5678') == 1234.5678


def test_str_if_not_none_returns_empty_string_for_none():
    assert str_if_not_none(None) == ''


def test_str_if_not_none_returns_string_for_float():
    assert str_if_not_none(1234.5678) == '1234.5678'


def test_str_if_not_none_returns_int_for_int():
    assert str_if_not_none(987654321) == '987654321'


def test_not_numeric_is_false_for_integer_input():
    assert not_numeric(13) is False


def test_not_numeric_is_false_for_float_input():
    assert not_numeric(13.12) is False


def test_not_numeric_is_false_for_integer_as_string_input():
    assert not_numeric('13') is False


def test_not_numeric_is_false_for_float_as_string_input():
    assert not_numeric('13.5') is False


def test_not_numeric_is_false_for_comma_float_as_string_input():
    assert not_numeric('13,5') is False


def test_not_numeric_is_true_for_non_number_input():
    assert not_numeric('abc') is True
