"""Module for basic utilities"""


def clear_args_dicts(args, kwargs):
    """Eliminates objects from parameters."""

    new_args = []
    allowed = [int, float, str]
    for arg in args:
        if type(arg) in allowed:
            new_args.append(arg)

    new_kwargs = {}
    for k, v in kwargs.items():
        if type(v) in allowed:
            new_kwargs[k] = v
            
    return new_args, new_kwargs