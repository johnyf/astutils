"""Abstract syntax tree nodes."""


class Terminal(object):
    """Nullary symbol."""

    def __init__(self, value, dtype='terminal'):
        try:
            value + 's'
        except TypeError:
            raise TypeError(
                'value must be a string, got: {v}'.format(v=value))
        self.type = dtype
        self.value = value

    def __repr__(self):
        return '{cls}({v}, {t})'.format(
            cls=type(self).__name__,
            t=self.type,
            v=repr(self.value))

    def __str__(self, *arg, **kw):
        return self.value

    def __len__(self):
        return 1

    def __eq__(self, other):
        return (self.type == other.type and
                self.value == other.value)

    def flatten(self, *arg, **kw):
        return self.value


class Operator(object):
    """Operator with arity > 0."""

    def __init__(self, operator, *operands):
        try:
            operator + 'a'
        except TypeError:
            raise TypeError(
                'operator must be string, got: {op}'.format(
                    op=operator))
        self.type = 'operator'
        self.operator = operator
        self.operands = list(operands)

    def __repr__(self):
        return '{cls}({op}, {xyz})'.format(
            cls=type(self).__name__,
            op=repr(self.operator),
            xyz=', '.join(repr(x) for x in self.operands))

    def __str__(self, depth=None):
        if depth is not None:
            depth -= 1
        if depth == 0:
            return '...'
        return '({op} {xyz})'.format(
            op=self.operator,
            xyz=' '.join(x.__str__(depth=depth)
                         for x in self.operands))

    def __len__(self):
        return 1 + sum(len(x) for x in self.operands)

    def flatten(self, *arg, **kw):
        return ' '.join([
            '(',
            self.operator,
            ', '.join(x.flatten(*arg, **kw) for x in self.operands),
            ')'])
