"""Example usage of `astutils` classes.

This file is `foo.lexyacc`, so that
`setup.py` can `from foo import lexyacc`.
"""
import astutils
from foo.ast import Nodes


TABMODULE = 'foo.calc_parsetab'


class Lexer(astutils.Lexer):
    """Lexer for Boolean formulae."""

    reserved = {
        'False': 'FALSE',
        'True': 'TRUE'}
    delimiters = ['LPAREN', 'RPAREN', 'COMMA']
    operators = ['NOT', 'AND', 'OR', 'XOR', 'IMP', 'BIMP',
                 'EQUALS', 'NEQUALS']
    misc = ['NAME', 'NUMBER']

    def t_NAME(self, t):
        r"[A-Za-z_][A-za-z0-9]*"
        t.type = self.reserved.get(t.value, 'NAME')
        return t

    def t_AND(self, t):
        r'\&\&'
        t.value = '&'
        return t

    def t_OR(self, t):
        r'\|\|'
        t.value = '|'
        return t

    t_NOT = r'\!'
    t_XOR = r'\^'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NUMBER = r'\d+'
    t_IMP = '->'
    t_BIMP = '\<->'
    t_ignore = " \t"

    def t_comment(self, t):
        r'\#.*'
        return

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")


class Parser(astutils.Parser):
    """Parser for Boolean formulae."""

    tabmodule = TABMODULE
    start = 'expr'
    # low to high
    precedence = (
        ('left', 'BIMP'),
        ('left', 'IMP'),
        ('left', 'XOR'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQUALS', 'NEQUALS'),
        ('right', 'NOT'))
    Lexer = Lexer
    nodes = Nodes

    def p_bool(self, p):
        """expr : TRUE
                | FALSE
        """
        p[0] = self.nodes.Bool(p[1])

    def p_number(self, p):
        """expr : NUMBER"""
        p[0] = self.nodes.Num(p[1])

    def p_var(self, p):
        """expr : NAME"""
        p[0] = self.nodes.Var(p[1])

    def p_unary(self, p):
        """expr : NOT expr"""
        p[0] = self.nodes.Unary(p[1], p[2])

    def p_binary(self, p):
        """expr : expr AND expr
                | expr OR expr
                | expr XOR expr
                | expr IMP expr
                | expr BIMP expr
                | expr EQUALS expr
                | expr NEQUALS expr
        """
        p[0] = self.nodes.Binary(p[2], p[1], p[3])

    def p_paren(self, p):
        """expr : LPAREN expr RPAREN"""
        p[0] = p[2]


def _rewrite_tables(outputdir='./'):
    astutils.rewrite_tables(Parser, TABMODULE, outputdir)


# this is a convenience to regenerate the tables
# during development
if __name__ == '__main__':
    _rewrite_tables()
