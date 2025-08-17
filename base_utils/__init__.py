"""Module for basic utilities."""


def clear_args_dicts(args: list, kwargs: dict) -> (list, dict):
    """Eliminates objects from parameters."""
    allowed = [int, float, str]

    new_args = [arg for arg in args if type(arg) in allowed]
    new_kwargs = {k: v for k, v in kwargs.items() if type(v) in allowed}

    return new_args, new_kwargs
