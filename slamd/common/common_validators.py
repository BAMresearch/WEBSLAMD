from slamd.common.slamd_utils import not_numeric


def validate_ranges(increment, max_value, min_value, constraint):
    # Returns *False* if range is invalid
    return min_value < 0 or min_value > constraint or max_value > constraint or min_value > max_value \
           or max_value < 0 or increment <= 0 or not_numeric(max_value) \
           or not_numeric(min_value) or not_numeric(increment)


def min_max_increment_config_valid(min_max_increments_values, constraint):
    for i in range(len(min_max_increments_values) - 1):
        min_value = float(min_max_increments_values[i]['min'])
        max_value = float(min_max_increments_values[i]['max'])
        increment = float(min_max_increments_values[i]['increment'])
        if validate_ranges(increment, max_value, min_value, float(constraint)):
            return False
    return True
