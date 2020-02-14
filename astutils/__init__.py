"""Utilities for abstract syntax trees and parsing with PLY."""
# Copyright 2014-2020 by California Institute of Technology
# All rights reserved. Licensed under 3-clause BSD.
#
from astutils.ast import Terminal, Operator
from astutils.ply import Lexer, Parser, rewrite_tables
try:
    from ._version import version as __version__
except:
    __version__ = None
