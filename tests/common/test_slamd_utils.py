from slamd.common.slamd_utils import empty, not_empty, join_all, molecular_formula_of, not_numeric


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


def test_molecular_formula_of_returns_original_input_if_no_numbers_are_present():
    assert molecular_formula_of('NaO') == 'NaO'


def test_molecular_formula_of_returns_subscripted_numbers():
    assert molecular_formula_of('Fe2O3') == u'Fe\u2082O\u2083'


def test_molecular_formula_of_returns_subsripted_numbers_for_complex_molecules():
    assert molecular_formula_of('C6H12') == u'C\u2086H\u2081\u2082'


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
