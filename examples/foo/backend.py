"""Example of subclassing the derived AST to change the flatteners.

This allows changing backend, without touching the
frontend (parser) in `lexyacc`.
"""
import foo.ast as _ast
import foo.lexyacc as _lexyacc


class Nodes(_ast.Nodes):
    """Further subclassing that changes selected flatteners."""

    class Var(_ast.Nodes.Var):
        def flatten(self, varmap=None):
            """Rename variable, if found in `varmap`."""
            if varmap is None:
                return self.value
            else:
                return varmap.get(self.value, self.value)

    class Binary(_ast.Nodes.Binary):
        def flatten(self, *arg, **kw):
            """Produce postfix syntax."""
            return ' '.join([
                '(',
                self.operands[0].flatten(*arg, **kw),
                self.operands[1].flatten(*arg, **kw),
                self.operator,
                ')'])


parser = _lexyacc.Parser(nodes=Nodes())
