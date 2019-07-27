import logging
import terminaltables


def get_stream_logger(name, write_type, rec_format):
    """Get stream logger :).

    :param name: str, name of logger
    :param write_type: int, type of write from logging (for example logging.DEBUG)
    :param rec_format: str, type of record with some rules by logging
    :return: logger object
    """

    logger = logging.getLogger(name)
    logger.setLevel(write_type)
    sh = logging.StreamHandler()
    formatter = logging.Formatter(rec_format)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger


def calc_salary(s_from, s_to):
    """Calc salary.
    First modify salary to get 'from', 'to'

    :param s_from: int, salary from
    :param s_to: int, salary to
    :return: int or None, size of salary by 'from' and 'to'
    """

    if (s_from is not None and s_to is not None):
        return (s_from + s_to) / 2

    # if we there that means 'from' or 'low' salary is None but only one
    # from is lowest salary of range, multiply by highly coefficient
    if s_from is not None:
        return s_from * 1.2

    # to is highest salary of range, multiply by lowly coefficient
    if s_to is not None:
        return s_to * 0.8

    return None


def get_pretty_table_from_dict(header, dictionary, title, keys_rules):
    """Function convert dictionary to pretty table.

    :param header: list, headers of table, must be bigger by one then keys_rules
    :param dictionary: dict, dictionary in next format:
    {
        key1: {
            subkey1: value1_1,
            subkey2: value1_2,
            subkey3: value1_3,
            ...
        },
        key2: {
            subkey1: value2_1,
            subkey2: value2_2,
            subkey3: value2_3,
            ...
        },
        ...
    }
    subkeys must be equal in every item of dict
    :param title: title of table
    :param keys_rules: list, list of subkeys, set order of cols in tables
    :return: str, pretty table for print
    """

    if not (len(header) - len(keys_rules) == 1):
        raise AttributeError('lenght of header must be bigger for one then len keys_rules')

    for k in dictionary:
        subdict_keys = set(dictionary[k].keys())

        if subdict_keys.difference(set(keys_rules)):
            raise AttributeError('keys_rules must be equal subdicts in dictionary')

    table = [header]
    for d_key, d_value in dictionary.items():
        raw = [d_key]
        for key in keys_rules:
            raw.append(d_value[key])
        table.append(raw)
    table_instance = terminaltables.AsciiTable(table, title)

    return table_instance.table
