[![Build Status][build_img]][ci]


About
=====

Bare essentials for building abstract syntax trees (AST) and Python
`lex`-`yacc` ([PLY](https://github.com/dabeaz/ply)) parsers.
The package includes:

- two classes for tree nodes: `Terminal`, `Operator`
- a `Lexer` and `Parser` class, and a helper function to erase and
  rewrite the table files.

The examples under `examples/` demonstrate how to use these classes to create
a richer AST, a parser, and different backends that use the same parser.

These classes provide the boilerplate for parsing with PLY, and are based on
code that was developed in [`tulip`](
    https://github.com/tulip-control/tulip-control)
and [`promela`](https://github.com/johnyf/promela).


License
=======
[BSD-3](https://opensource.org/licenses/BSD-3-Clause), see file `LICENSE`.


[build_img]: https://github.com/johnyf/astutils/actions/workflows/main.yml/badge.svg?branch=main
[ci]: https://github.com/johnyf/astutils/actions
