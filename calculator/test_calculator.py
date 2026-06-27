
import sys
sys.path.append('pkg')

from calculator import Calculator

calc = Calculator()

test_expressions = {
    "2 + 3 * 4": 14.0,
    "2 * 3 + 4": 10.0,
    "10 / 2 - 1": 4.0,
    "1": 1.0,
    "   ": None,
    "": None,
    "2 +": ValueError,
    "2 + a": ValueError,
}

for expr, expected in test_expressions.items():
    try:
        result = calc.evaluate(expr)
        print(f"Expression: '{expr}', Result: {result}, Expected: {expected}")
        assert result == expected, f"Failed for '{expr}'. Got {result}, expected {expected}"
    except Exception as e:
        print(f"Expression: '{expr}', Error: {type(e).__name__}, Expected: {expected.__name__ if expected else None}")
        assert type(e) == expected, f"Failed for '{expr}'. Got {type(e).__name__}, expected {expected.__name__ if expected else None}"

print("All tests passed!")
