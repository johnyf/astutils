"""Utilities for Python lex-yacc (PLY)."""
# Copyright 2014-2022 by California Institute of Technology
# All rights reserved. Licensed under 3-clause BSD.
#
import logging
import os
import textwrap as _tw
import typing as _ty
import warnings

import ply.lex
import ply.yacc

import astutils.ast as _ast


logger = logging.getLogger(__name__)


class Lexer:
    """Init and build methods."""

    def __init__(
            self,
            debug:
                bool=False
            ) -> None:
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

    def t_error(
            self,
            t
            ) -> _ty.NoReturn:
        raise RuntimeError(
            f'Illegal character "{t.value[0]}"')

    def build(
            self,
            debug:
                bool=False,
            debuglog=None,
            **kwargs
            ) -> None:
        """Create a lexer."""
        if debug and debuglog is None:
            debuglog = self.logger
        self.lexer = ply.lex.lex(
            module=self,
            debug=debug,
            debuglog=debuglog,
            **kwargs)


class Parser:
    """Init, build and parse methods.

    To subclass, overwrite the class attributes
    defined below, and add production rules.
    """

    def __init__(
            self,
            nodes=None,
            lexer=None
            ) -> None:
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
            tabmodule:
                str |
                None=None,
            outputdir:
                str='',
            write_tables:
                bool=False,
            debug:
                bool=False,
            debuglog=None
            ) -> None:
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
            formula:
                str,
            debuglog=None
            ) -> _ty.Any:
        """Parse string `formula`.

        @param formula:
            input to the parser
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
        self._clear_lr_stack()
        if root is not None:
            return root
        raise RuntimeError(
            f'failed to parse:\n\t{formula}')

    def _clear_lr_stack(
            self
            ) -> None:
        """Ensure no references remain.

        Otherwise, references can prevent `gc` from
        collecting objects that are expected to
        have become unreachable.
        """
        has_lr_stack = (
            self.parser is not None and
            hasattr(self.parser, 'statestack') and
            hasattr(self.parser, 'symstack'))
        if not has_lr_stack:
            return
        self.parser.restart()

    def p_error(
            self,
            p
            ) -> _ty.NoReturn:
        s = list()
        while True:
            tok = self.parser.token()
            if tok is None:
                break
            s.append(tok.value)
        s = ' '.join(s)
        raise RuntimeError(
            f'Syntax error at "{p.value}"\n'
            f'remaining input:\n{s}\n')


def rewrite_tables(
        parser_class:
            type[Parser],
        tabmodule:
            str,
        outputdir:
            str
        ) -> None:
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
    @param outputdir:
        dump parser file
        in this directory
    """
    if outputdir is None:
        raise ValueError(
            '`outputdir` must be `str`.')
    *_, table = tabmodule.rpartition('.')
    for ext in ('.py', '.pyc'):
        path = outputdir + table + ext
        if os.path.isfile(path):
            logger.info(f'found file `{path}`')
            os.remove(path)
            logger.info(f'removed file `{path}`')
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
