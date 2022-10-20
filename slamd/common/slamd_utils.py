from slamd.common.error_handling import ValueNotSupportedException, SlamdUnprocessableEntityException


def empty(input_value):
    if isinstance(input_value, (int, float)):
        return False
    return input_value is None or input_value == ''


def not_empty(input_value):
    return not empty(input_value)


def join_all(input_list):
    if input_list is None:
        return ''
    return ''.join(input_list)


def molecular_formula_of(input_molecule):
    """
    input_molecule: pass molecule as simple string such as H20 to get it back in proper chemical notation
    """
    subscript = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
    return input_molecule.translate(subscript)


def not_numeric(input_value):
    return not numeric(input_value)


def numeric(input_value):
    if isinstance(input_value, (int, float)):
        return True
    if _pieces_are_numeric(input_value, '.') or _pieces_are_numeric(input_value, ','):
        return True
    return False


def string_to_number(input_value):
    if not_numeric(input_value):
        raise ValueNotSupportedException(f'Cannot process input. {input_value} should be a number!')
    if isinstance(input_value, (int, float)):
        return float(input_value)
    if ',' not in input_value:
        return float(input_value)
    input_as_number = input_value.replace(',', '.')
    return float(input_as_number)


def string_to_number_or_string(input_value):
    if not_numeric(input_value):
        return input_value
    return string_to_number(input_value)


def _pieces_are_numeric(input_value, separator):
    pieces = input_value.split(separator)
    if len(pieces) == 1:
        return input_value.isnumeric()
    if len(pieces) == 2:
        return pieces[0].isnumeric() and pieces[1].isnumeric()
    return False


def float_if_not_empty(input_value):
    return float(input_value) if not_empty(input_value) else None


def str_if_not_none(input_value):
    return str(input_value) if input_value is not None else ''


def write_dict_into_object(dictionary, target_object):
    for key in target_object.__dict__.keys():
        if key not in dictionary:
            raise SlamdUnprocessableEntityException(message=f'Error while attempting to write values into '
                                                            f'object: Expected key {key}, got '
                                                            f'keys {list(dictionary.keys())}')

        target_object.__dict__[key] = dictionary[key]
