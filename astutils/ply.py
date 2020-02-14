"""Utilities for Python lex-yacc (PLY)."""
# Copyright 2014-2020 by California Institute of Technology
# All rights reserved. Licensed under 3-clause BSD.
#
from __future__ import absolute_import
import logging
import os

import ply.lex
import ply.yacc

from astutils import ast as nodes


logger = logging.getLogger(__name__)


class Lexer(object):
    """Init and build methods."""

    reserved = dict()
    delimiters = list()
    operators = list()
    misc = list()
    logger = logger

    def __init__(self, debug=False):
        self.tokens = (
            self.delimiters + self.operators +
            self.misc + list(set(self.reserved.values())))
        self.build(debug=debug)

    def t_error(self, t):
        raise Exception('Illegal character "{t}"'.format(t=t.value[0]))

    def build(self, debug=False, debuglog=None, **kwargs):
        """Create a lexer."""
        if debug and debuglog is None:
            debuglog = self.logger
        self.lexer = ply.lex.lex(
            module=self,
            debug=debug,
            debuglog=debuglog,
            **kwargs)


class Parser(object):
    """Init, build and parse methods.

    To subclass, overwrite the class attributes
    defined below, and add production rules.
    """

    tabmodule = ''
    start = 'expr'
    # low to high
    precedence = tuple()
    Lexer = Lexer
    nodes = nodes
    logger = logger

    def __init__(self, nodes=None, lexer=None):
        if nodes is not None:
            self.nodes = nodes
        if lexer is None:
            lexer = self.Lexer()
        self.lexer = lexer
        self.tokens = self.lexer.tokens
        self.build()

    def build(self, tabmodule=None, outputdir='', write_tables=False,
              debug=False, debuglog=None):
        """Build parser using `ply.yacc`."""
        if tabmodule is None:
            tabmodule = self.tabmodule
        if debug and debuglog is None:
            debuglog = self.logger
        self.parser = ply.yacc.yacc(
            method='LALR',
            module=self,
            start=self.start,
            tabmodule=tabmodule,
            outputdir=outputdir,
            write_tables=write_tables,
            debug=debug,
            debuglog=debuglog)

    def parse(self, formula, debuglog=None):
        """Parse formula string and create abstract syntax tree (AST)."""
        root = self.parser.parse(
            input=formula,
            lexer=self.lexer.lexer,
            debug=debuglog)
        if root is None:
            raise Exception('failed to parse:\n\t{f}'.format(f=formula))
        return root

    def p_error(self, p):
        s = list()
        while True:
            tok = self.parser.token()
            if tok is None:
                break
            s.append(tok.value)
        raise Exception(
            'Syntax error at "{p}"\n'.format(p=p.value) +
            'remaining input:\n{s}\n'.format(s=' '.join(s)))


def rewrite_tables(Parser, tabmodule, outputdir):
    """Write the parser table file, even if it exists.

    The module name (after last dot) in `tabmodule`
    is appended to `outputdir` to form the path.

    @param Parser: PLY production rules
    @param tabmodule: module name for table file
    @type tabmodule: `str`
    @param outputdir: dump parser file in this directory
    @type outputdir: `str`
    """
    table = tabmodule.split('.')[-1]
    for ext in ('.py', '.pyc'):
        try:
            os.remove(outputdir + table + ext)
        except:
            pass
    parser = Parser()
    parser.build(
        write_tables=True,
        outputdir=outputdir,
        tabmodule=table,
        debug=True)


# example use:
# if __name__ == '__main__':
#    rewrite_tables(Parser, TABMODULE, outputdir)
