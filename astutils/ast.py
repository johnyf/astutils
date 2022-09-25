"""Abstract syntax tree nodes."""
# Copyright 2014-2022 by California Institute of Technology
# All rights reserved. Licensed under 3-clause BSD.
#


class Terminal:
    """Nullary symbol."""

    def __init__(
            self,
            value:
                str,
            dtype:
                str='terminal'
            ) -> None:
        try:
            value + 's'
        except TypeError:
            raise TypeError(
                'value must be a string, '
                f'got: {value}')
        self.type = dtype
        self.value = value

    def __hash__(
            self
            ) -> int:
        return id(self)

    def __repr__(
            self
            ) -> str:
        class_name = type(self).__name__
        return (
            f'{class_name}('
                f'{self.value!r}, '
                f'{self.type!r})')

    def __str__(
            self,
            *arg,
            **kw
            ) -> str:
        return self.value

    def __len__(
            self
            ) -> int:
        return 1

    def __eq__(
            self,
            other
            ) -> bool:
        return (
            hasattr(other, 'type') and
            hasattr(other, 'value') and
            self.type == other.type and
            self.value == other.value)

    def flatten(
            self,
            *arg,
            **kw):
        return self.value


class Operator:
    """Operator with arity > 0."""

    def __init__(
            self,
            operator:
                str,
            *operands
            ) -> None:
        try:
            operator + 'a'
        except TypeError:
            raise TypeError(
                'operator must be string, '
                f'got: {operator}')
        self.type = 'operator'
        self.operator = operator
        self.operands = list(operands)

    def __repr__(
            self
            ) -> str:
        class_name = type(self).__name__
        xyz = ', '.join(map(repr, self.operands))
        return (
            f'{class_name}('
                f'{self.operator!r}, '
                f'{xyz})')

    def __str__(
            self
            ) -> str:
        xyz = ' '.join(map(str, self.operands))
        return f'({self.operator} {xyz})'

    def __len__(
            self
            ) -> int:
        return 1 + sum(map(len, self.operands))

    def flatten(
            self,
            *arg,
            **kw):
        csv = ', '.join(
            x.flatten(*arg, **kw)
            for x in self.operands)
        return f'( {self.operator} {csv} )'
