"""Module for basic utilities"""
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession


def clear_args_dicts(args, kwargs):
    """Eliminates objects from parameters."""

    new_args = []
    ignored = [AsyncSession, ClientSession]
    for arg in args:
        to_be_ignored = False
        for ignore in ignored:
            if isinstance(arg, ignore):
                to_be_ignored = True
                break
        if not to_be_ignored:
            new_args.append(arg)

    new_kwargs = {}
    for k, v in kwargs.items():
        to_be_ignored = False
        for ignore in ignored:
            if isinstance(v, ignore):
                to_be_ignored = True
                break
        if not to_be_ignored:
            new_kwargs[k] = v
            
    return new_args, new_kwargs