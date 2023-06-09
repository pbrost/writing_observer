'''
This file includes commands to create a request within the
communication protocol. It provides a set of Python calls, designed to
(roughly) mirror a relational database, and returns a JSON object
corresponding to that query.

See the examples in the `tests.py` for the format.

This JSON object can then be executed by executor.py.

This file should be kept thin and minimal, since we will want versions
translated into JavaScript for the front end (and, perhaps eventually,
Julia, R, Stata, and other languages researchers might want to use to
query our system).

This file is intended to be imported in diverse contexts, including ones
where we don't want all of the machinery of the Learning Observer, so also
note the lack of dependencies.
'''

dispatch = "dispatch"


class DISPATCH_MODES:
    pass


dispatch_modes = ['parameter', 'variable', 'call', 'select', 'join', 'map', 'keys']
[setattr(DISPATCH_MODES, d.upper(), d) for d in dispatch_modes]


def parameter(parameter_name):
    """
    Returns a dictionary with the given parameter_name.

    :param parameter_name: the name of the parameter
    :type parameter_name: str
    :return: a dictionary containing the dispatch type and the parameter name
    :rtype: dict
    """
    return {
        dispatch: DISPATCH_MODES.PARAMETER,
        "parameter_name": parameter_name
    }


def variable(variable_name):
    """
    Returns a dictionary with the given variable_name.

    :param variable_name: the name of the variable
    :type variable_name: str
    :return: a dictionary containing the dispatch type and the variable name
    :rtype: dict
    """
    return {
        dispatch: DISPATCH_MODES.VARIABLE,
        "variable_name": variable_name
    }


def call(function_name):
    """
    Returns a callable that, when invoked, returns a dictionary containing the dispatch type, function name, arguments, and keyword arguments.

    :param function_name: the name of the function to call
    :type function_name: str
    :return: a callable object
    """
    def caller(*args, **kwargs):
        return {
            dispatch: DISPATCH_MODES.CALL,
            "function_name": function_name,
            "args": args,
            "kwargs": kwargs
        }
    setattr(caller, "__lo_name__", function_name)
    return caller


def select(keys, fields=None):
    """
    Returns a dictionary with the given keys.

    :param keys: the keys to select
    :type keys: list
    :return: a dictionary containing the dispatch type and the keys
    :rtype: dict
    """
    return {
        dispatch: DISPATCH_MODES.SELECT,
        "keys": keys,
        "fields": fields
    }


def join(LEFT, RIGHT, LEFT_ON=None, RIGHT_ON=None):
    """
    Returns a dictionary representing a JOIN operation between LEFT and RIGHT based on LEFT_ON and RIGHT_ON.

    :param LEFT: the left table
    :type LEFT: dict
    :param RIGHT: the right table
    :type RIGHT: dict
    :param LEFT_ON: the key to join on from the left table
    :type LEFT_ON: str
    :param RIGHT_ON: the key to join on from the right table
    :type RIGHT_ON: str
    :return: a dictionary containing the dispatch type and the join information
    :rtype: dict
    """
    return {
        dispatch: DISPATCH_MODES.JOIN,
        "left": LEFT,
        "right": RIGHT,
        "left_on": LEFT_ON,
        "right_on": RIGHT_ON
    }


def map(function, values, value_path=None):
    """
    Returns a dictionary representing a MAP operation for the given function and values.

    :param function: the function to map
    :type function: callable
    :param values: the values to map over
    :type values: list
    :param value_path: path to values that should be ran through map function
    :type value_path: str
    :return: a dictionary containing the dispatch type, the function name, and the values
    :rtype: dict
    """
    return {
        dispatch: DISPATCH_MODES.MAP,
        "function": function.__lo_name__,
        "values": values,
        "value_path": value_path
    }


def keys(func, **kwargs):
    """
    Some way to make keys. This is a placeholder function and needs to be implemented.

    :param text: text to generate keys from
    :type text: str
    :param doc_ids: document IDs to generate keys from
    :type doc_ids: list
    :param value_path: path to values that should be ran through map function
    :type value_path: str
    :return: a dictionary representing the keys
    :rtype: dict
    """
    return {
        "dispatch": DISPATCH_MODES.KEYS,
        "function": func,
        **kwargs
    }
