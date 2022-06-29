def empty(input):
    return input is None or input == ''


def not_empty(input):
    return not empty(input)


def join_all(input_list):
    return ''.join(input for input in input_list)
