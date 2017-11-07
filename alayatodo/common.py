def empty(str_value):
    return str_value is None or str_value.strip() == ''


def str_to_int(str_value, default):
    if empty(str_value):
        return default
    try:
        return int(str_value)
    except ValueError:
        return default
