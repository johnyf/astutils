"""Utilities for Python lex-yacc (PLY)."""
# Copyright 2014-2022 by California Institute of Technology
# All rights reserved. Licensed under 3-clause BSD.
#
from __future__ import absolute_import
import logging
import os
import textwrap as _tw
import warnings

import ply.lex
import ply.yacc

import astutils.ast as _ast


logger = logging.getLogger(__name__)


class Lexer(object):
    """Init and build methods."""

    def __init__(self, debug=False):
        self.reserved = getattr(
            self, 'reserved', dict())
        self.delimiters = getattr(
            self, 'delimiters', list())
        self.operators = getattr(
            self, 'operators', list())
        self.misc = getattr(
            self, 'misc', list())
        self.logger = getattr(
            self, 'logger', logger)
        self.tokens = (
            self.delimiters +
            self.operators +
            self.misc +
            sorted(set(self.reserved.values())))
        self.build(debug=debug)

    def t_error(self, t):
        raise Exception(
            'Illegal character "{t}"'.format(
                t=t.value[0]))

    def build(
            self,
            debug=False,
            debuglog=None,
            **kwargs):
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

    def __init__(
            self,
            nodes=None,
            lexer=None):
        self.tabmodule = getattr(
            self, 'tabmodule', None)
        self.start = getattr(
            self, 'start', 'expr')
        # low to high
        self.precedence = getattr(
            self, 'precedence', tuple())
        self.nodes = getattr(
            self, 'nodes', _ast)
        self.logger = getattr(
            self, 'logger', logger)
        if nodes is not None:
            self.nodes = nodes
        if lexer is not None:
            self._lexer = lexer
        elif hasattr(self, 'Lexer'):
            warnings.warn(_tw.dedent(f'''
                The parser attribute `Lexer`
                has been deprecated. Instead,
                pass argument `lexer`, for example:

                ```py
                lexer = Lexer()
                super().__init__(lexer=lexer)
                ```
                '''),
                DeprecationWarning)
            self._lexer = self.Lexer()
        else:
            raise ValueError(
                'pass argument `lexer` to '
                '`Parser.__init__()`')
        self.tokens = self._lexer.tokens
        self.parser = None

    def build(
            self,
            tabmodule=None,
            outputdir='',
            write_tables=False,
            debug=False,
            debuglog=None):
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

    def parse(
            self,
            formula,
            debuglog=None):
        """Parse string `formula`.

        @param formula:
            input to the parser
        @type formula:
            `str`
        @return:
            what the parser returns
            (many parsers return a syntax tree)
        """
        if self.parser is None:
            self.build()
        root = self.parser.parse(
            input=formula,
            lexer=self._lexer.lexer,
            debug=debuglog)
        if root is not None:
            return root
        raise Exception(
            'failed to parse:\n\t{f}'.format(
                f=formula))

    def p_error(self, p):
        s = list()
        while True:
            tok = self.parser.token()
            if tok is None:
                break
            s.append(tok.value)
        raise Exception(
            'Syntax error at "{p}"\n'.format(
                p=p.value) +
            'remaining input:\n{s}\n'.format(
                s=' '.join(s)))


def rewrite_tables(
        parser_class,
        tabmodule,
        outputdir):
    """Write the parser table file.

    Overwrites any preexisting parser file.

    The module name (after last dot) in `tabmodule`
    is appended to `outputdir` to form the path.

    Example use:

    ```python
    _TABMODULE = 'packagename.modulename_parsetab'


    class Parser(...):
        ...


    if __name__ == '__main__':
        outputdir = './'
        rewrite_tables(Parser, _TABMODULE, outputdir)
    ```

    @param parser_class:
        PLY production rules
    @param tabmodule:
        module name for table file
    @type tabmodule:
        `str`
    @param outputdir:
        dump parser file
        in this directory
    @type outputdir:
        `str`
    """
    if outputdir is None:
        raise ValueError(
            '`outputdir` must be `str`.')
    table = tabmodule.rpartition('.')[-1]
    for ext in ('.py', '.pyc'):
        path = outputdir + table + ext
        if os.path.isfile(path):
            logger.info(
                'found file `{path}`'.format(
                    path=path))
            os.remove(path)
            logger.info(
                'removed file `{path}`'.format(
                    path=path))
    parser = parser_class()
    debugfile = ply.yacc.debug_file
    path = os.path.join(outputdir, debugfile)
    with open(path, 'w') as debuglog_file:
        debuglog = ply.yacc.PlyLogger(debuglog_file)
        parser.build(
            write_tables=True,
            outputdir=outputdir,
            tabmodule=table,
            debug=True,
            debuglog=debuglog)
