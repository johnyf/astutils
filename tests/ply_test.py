import os

import astutils.ply
import pytest


class Lexer(astutils.ply.Lexer):

    def __init__(self, **kw):
        self.operators = ['NOT', 'AND']
        self.misc = ['NAME']
        super(Lexer, self).__init__(**kw)

    t_NAME = r'[A-Za-z_][A-za-z0-9]*'
    t_NOT = r'~'
    t_AND = r'/\\'
    t_ignore = ' \t'


class Parser(astutils.ply.Parser):

    def __init__(self, **kw):
        self.tabmodule = 'testing_parsetab'
        self.start = 'expr'
        self.precedence = (
            ('left', 'AND'),
            ('right', 'NOT'))
        kw.setdefault('lexer', Lexer())
        super(Parser, self).__init__(**kw)

    def p_not(self, p):
        """expr : NOT expr"""
        p[0] = not p[2]

    def p_and(self, p):
        """expr : expr AND expr"""
        p[0] = p[1] and p[3]

    def p_name(self, p):
        """expr : NAME"""
        s = p[1]
        p[0] = self.names[s]


def test_parser():
    parser = Parser()
    parser.names = {'True': True, 'False': False}
    s = 'True'
    r = parser.parse(s)
    assert r is True, r
    s = r'True /\ True'
    r = parser.parse(s)
    assert r is True, r
    s = r'False /\ True'
    r = parser.parse(s)
    assert r is False, r
    s = r'~ False /\ ~ True'
    r = parser.parse(s)
    assert r is False, r
    s = r'~ False /\ True'
    r = parser.parse(s)
    assert r is True, r


def test_illegal_character():
    parser = Parser()
    parser.names = {'True': True}
    s = '( True'
    with pytest.raises(RuntimeError):
        parser.parse(s)


def test_syntax_error():
    parser = Parser()
    parser.names = {'True': True}
    s = 'True True'
    with pytest.raises(RuntimeError):
        parser.parse(s)


def test_rewrite_tables():
    prefix = 'foo'
    outputdir = './'
    for ext in ('.py', '.pyc'):
        try:
            os.remove(prefix + ext)
        except:
            pass
    f = prefix + '.py'
    assert not os.path.isfile(f)
    astutils.ply.rewrite_tables(
        Parser, prefix, outputdir)
    assert os.path.isfile(f)
