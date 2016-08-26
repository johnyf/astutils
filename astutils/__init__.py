"""Utilities for abstract syntax trees and parsing with PLY."""
from astutils.ast import Terminal, Operator
from astutils.ply import Lexer, Parser, rewrite_tables
try:
    from ._version import version as __version__
except:
    __version__ = None
