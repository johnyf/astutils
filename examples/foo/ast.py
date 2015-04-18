"""Examples of subclassing the basic AST node classes.

The main purpose of subclassing is to create
different flattening methods. By creating a larger
variety of AST node classes, the same parser can
be used with different backends. Each backend is
created by subclassing the below classes, then
overriding the `flatten` method.
"""
import astutils


class Nodes(object):
    """Container of AST node classes for further subclassing."""

    Terminal = astutils.Terminal
    Operator = astutils.Operator

    class Var(astutils.Terminal):
        """Variable identifier."""

        def __init__(self, value, dtype='var'):
            super(Nodes.Var, self).__init__(value, dtype)

    class Bool(astutils.Terminal):
        """Boolean constant."""

        def __init__(self, value, dtype='bool'):
            super(Nodes.Bool, self).__init__(value, dtype)

    class Num(astutils.Terminal):
        """Numerical costant."""

        def __init__(self, value, dtype='num'):
            super(Nodes.Num, self).__init__(value, dtype)

    class Unary(astutils.Operator):
        """Unary operator."""

    class Binary(astutils.Operator):
        """Binary operator."""

        def flatten(self, *arg, **kw):
            return ' '.join([
                '(',
                self.operands[0].flatten(*arg, **kw),
                self.operator,
                self.operands[1].flatten(*arg, **kw),
                ')'])
