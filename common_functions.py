import logging
import terminaltables


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


def get_pretty_table_from_dict(header, dictionary, title, keys_rules, table_type='AsciiTable'):
    """Function convert dictionary to pretty table.

    :param header: list, headers of table, must be bigger by one then keys_rules
    :param dictionary: dict, dictionary in next format:

    # key_i - some key of dictionary, cause dictionaries have no order
    # Cell[i,j] - Cell of result table with i raw and j column. i and j starts from 1
    {
        Cell[1,1]: {
            keys_rules[0]: Cell[1,2],
            keys_rules[1]: Cell[1,3],
            ...
        },
        Cell[2,1]: {
            keys_rules[0]: Cell[2,2],
            keys_rules[1]: Cell[2,3],
            ...
        },
        ...
    }
    In this way dictionary has string keys and dict as values.
    Every value must have similar keys which must be written in keys rules which set order of table columns

    :param title: title of table
    :param keys_rules: list, list of subkeys, set order of cols in tables
    :param table_type: type of table from terminaltables
    in terminaltables==3.1.0 have 3 variants with title:
    AsciiTable, DoubleTable, SingleTable
    For the more information please read terminaltables documentation
    :return: str, pretty table for print, for example is:

    # j - some index of list
    # table_type == 'AsciiTable'
    # -1 - last index

    +title------------------+--------------------+---------------------+
    | header[0]             | header[j-1]        | header[-1]          |
    +-----------------------+--------------------+---------------------+
    | Cell[1,1]             | Cell[1,j]          | Cell[1,-1]          |
    | Cell[2,1]             | Cell[2,j]          | Cell[2,-1]          |
    | ...                   | ...                | ...                 |
    +-----------------------+--------------------+---------------------+
    """

    if not (len(header) - len(keys_rules) == 1):
        raise AttributeError('lenght of header must be bigger for one then len keys_rules')

    for key, value in dictionary.items():
        subdict_keys = set(value.keys())

        if subdict_keys.difference(set(keys_rules)):
            raise AttributeError('keys_rules must be equal subdicts in dictionary')

    valid_table_names = ['AsciiTable', 'DoubleTable', 'SingleTable']
    if table_type not in valid_table_names:
        raise AttributeError('unknown table type, set one of: {}'.format(', '.join(valid_table_names)))

    table = [header]
    for d_key, d_value in dictionary.items():
        raw = [d_key]
        for key in keys_rules:
            # user can use list or other structures
            raw.append(str(d_value[key]))
        table.append(raw)

    if table_type == 'AsciiTable':
        table_instance = terminaltables.AsciiTable(table, title)

    if table_type == 'DoubleTable':
        table_instance = terminaltables.DoubleTable(table, title)

    if table_type == 'SingleTable':
        table_instance = terminaltables.SingleTable(table, title)

    return table_instance.table
