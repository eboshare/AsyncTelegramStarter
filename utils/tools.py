import types


def function_fullname(function: types.FunctionType) -> str:
    return f'{function.__module__}.{function.__name__}'
