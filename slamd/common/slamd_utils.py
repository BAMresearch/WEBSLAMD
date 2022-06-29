def empty(input):
    return input is None or input == ''


def not_empty(input):
    return not empty(input)


def join_all(base_string, input_list):
    return base_string.join(input for input in input_list)
