"""Handlers package."""

from maxapi import Dispatcher

from .help import register_help_handlers
from .start import register_start_handlers


def register_handlers(dp: Dispatcher) -> None:
    register_start_handlers(dp)
    register_help_handlers(dp)


__all__ = ["register_handlers"]
