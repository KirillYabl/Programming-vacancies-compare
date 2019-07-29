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


def get_pretty_table_from_dict(attributes_titles, dictionary, title, attributes_to_print_order,
                               table_type='AsciiTable'):
    """Function convert dictionary to pretty table.

    :param attributes_titles: list, headers of table, must be bigger by one then attributes_to_print
    :param dictionary: dict, dictionary in next format: (for example legendary boxers table :) )

    {
        "Mike Tyson": {
            "Total_fights": 58,
            "Wins": 50,
            ...
        },
        "Muhammad Ali": {
            "Total fights": 61,
            "Wins": 56,
            ...
        },
        ...
    }
    In this way dictionary has string as keys and dict as values.
    Every value as dict must have similar keys which must be written in keys rules which set order of table columns

    :param title: title of table
    :param attributes_to_print_order: list, list of attributes which set order of cols in tables
    :param table_type: type of table from terminaltables
    in terminaltables==3.1.0 have 3 variants with title:
    AsciiTable, DoubleTable, SingleTable
    For the more information please read terminaltables documentation
    :return: str, pretty table for print, for example is:

    # table_type == 'AsciiTable'
    # attributes_titles == ["Boxer name", "Total fights", "Wins"]
    # attributes_to_print_order == ["Total_fights", "Wins"]
    # title == "Legendary Boxers"

    +Legendary Boxers-------+----------------------+----------------------+----------------------+
    | Boxer name            | Total fights         | Wins                 | ...                  |
    +-----------------------+----------------------+----------------------+----------------------+
    | Muhammad Ali          | 61                   | 56                   | ...                  |
    | Mike Tyson            | 58                   | 50                   | ...                  |
    | ...                   | ...                  | ...                  | ...                  |
    +-----------------------+----------------------+----------------------+----------------------+
    """

    if not (len(attributes_titles) - len(attributes_to_print_order) == 1):
        raise AttributeError('lenght of header must be bigger for one then len keys_rules')

    for key, value in dictionary.items():
        subdict_keys = set(value.keys())

        if subdict_keys.difference(set(attributes_to_print_order)):
            raise AttributeError('keys_rules must be equal subdicts in dictionary')

    valid_table_names = ['AsciiTable', 'DoubleTable', 'SingleTable']
    if table_type not in valid_table_names:
        raise AttributeError('unknown table type, set one of: {}'.format(', '.join(valid_table_names)))

    table = [attributes_titles]
    for d_key, d_value in dictionary.items():
        raw = [d_key]
        for key in attributes_to_print_order:
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
