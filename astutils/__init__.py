"""Utilities for abstract syntax trees and parsing with PLY."""
# Copyright 2014-2022 by California Institute of Technology
# All rights reserved. Licensed under 3-clause BSD.
#
from astutils.ast import Terminal, Operator
from astutils.ply import Lexer, Parser, rewrite_tables
try:
    from ._version import version as __version__
except ImportError:
    __version__ = None
