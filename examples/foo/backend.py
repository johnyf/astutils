"""Example of subclassing the derived AST to change the flatteners.

This allows changing backend, without touching the
frontend (parser) in `lexyacc`.
"""
from foo.ast import Nodes as _Nodes
from foo import lexyacc


class Nodes(_Nodes):
    """Further subclassing that changes selected flatteners."""

    class Var(_Nodes.Var):
        def flatten(self, varmap=None):
            """Rename variable, if found in `varmap`."""
            if varmap is None:
                return self.value
            else:
                return varmap.get(self.value, self.value)

    class Binary(_Nodes.Binary):
        def flatten(self, *arg, **kw):
            """Produce postfix syntax."""
            return ' '.join([
                '(',
                self.operands[0].flatten(*arg, **kw),
                self.operands[1].flatten(*arg, **kw),
                self.operator,
                ')'])


parser = lexyacc.Parser(nodes=Nodes())
