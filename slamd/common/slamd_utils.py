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
