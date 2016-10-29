from astutils import ast


def test_terminal():
    value = 'a'
    t = ast.Terminal(value)
    r = repr(t)
    assert r == "Terminal('a', terminal)", r
    r = str(t)
    assert r == 'a', r
    r = len(t)
    assert r == 1, r
    p = ast.Terminal(value)
    assert t == p, (t, p)
    p = ast.Terminal('b')
    assert t != p, (t, p)
    p = ast.Terminal(value, 'number')
    assert t != p, (t, p)
    r = t.flatten()
    assert r == value, r


def test_operator():
    a = ast.Terminal('a')
    b = ast.Terminal('b')
    op = '+'
    operands = [a, b]  # 'a', 'b' fail due to `str`
    t = ast.Operator(op, *operands)
    r = repr(t)
    r_ = (
        "Operator('+', "
        "Terminal('a', terminal), "
        "Terminal('b', terminal))")
    assert r == r_, r
    r = str(t)
    assert r == '(+ a b)', r
    r = len(t)
    assert r == 3, r
    r = t.flatten()
    assert r == '( + a, b )', r
