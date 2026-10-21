from calculator import calculator


def test_arithmetic():
    calc = calculator()
    assert calc.calculate("do 2 + 2") == "result is 4"
    assert calc.calculate("do 5 - 3") == "result is 2"
    assert calc.calculate("do 3 * 4") == "result is 12"
    assert calc.calculate("do 8 / 2") == "result is 4"
    assert calc.calculate("do 8 / 3") == "result is 2"


def test_invalid_arithmetic_does_not_crash():
    calc = calculator()
    assert calc.calculate("do") == "invalid operation"
    assert calc.calculate("do 1") == "invalid operation"
    assert calc.calculate("do 8 / 0") == "invalid operation"
    assert calc.calculate("do foo + bar") == "invalid operation"
    assert calc.calculate("do 2 ^ 2") == "invalid operation"
