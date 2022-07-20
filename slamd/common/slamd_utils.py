def empty(input):
    return input is None or input == ''


def not_empty(input):
    return not empty(input)


def join_all(input_list):
    if input_list is None:
        return ''
    return ''.join(input_list)


def molecular_formula_of(input_molecule):
    """
    input_molecule: pass molecule as simple string such as H20 to get it back in proper chemical notation
    """
    subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return input_molecule.translate(subscript)


def not_numeric(input_value):
    if isinstance(input_value, (int, float)):
        return False
    return not input_value.isnumeric()


def float_if_not_empty(input_value):
    return float(input_value) if not_empty(input_value) else None


def str_if_not_none(input_value):
    return str(input_value) if input_value is not None else ''
