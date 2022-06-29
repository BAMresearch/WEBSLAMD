def empty(input):
    return input is None or input == ''


def not_empty(input):
    return not empty(input)


def join_all(input_list):
    if input_list is None:
        return ''
    return ''.join(input for input in input_list)


def symbol_of(input_molecule):
    """
    input_molecule: pass molecule as simple string such as H20 to get in back in proper chemical notation
    """
    individual_chars = [char for char in input_molecule]
    result = ''
    for char in individual_chars:
        if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if char == '0':
                result += u'\u2080'
            elif char == '1':
                result += u'\u2081'
            elif char == '2':
                result += u'\u2082'
            elif char == '3':
                result += u'\u2083'
            elif char == '4':
                result += u'\u2084'
            elif char == '5':
                result += u'\u2085'
            elif char == '6':
                result += u'\u2086'
            elif char == '7':
                result += u'\u2087'
            elif char == '8':
                result += u'\u2088'
            else:
                result += u'\u2089'
        else:
            result += char
    return result
