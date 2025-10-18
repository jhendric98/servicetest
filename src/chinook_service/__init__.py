"""Chinook Service - Flask REST API for the Chinook sample database."""

from __future__ import annotations

from .server import create_app, main

__version__ = "0.1.0"
__all__ = ["create_app", "main"]
