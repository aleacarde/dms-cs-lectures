import pytest

from src.Lecture1.Lecture1 import NaturalNumber

def setup_function():
    global zero, one, two, three, four
    zero = NaturalNumber(0)
    one = zero.successor()
    two = one.successor()
    three = two.successor()
    four = three.successor()

def test_initialization():
    # Test initialization of NaturalNumber
    with pytest.raises(ValueError):
        NaturalNumber(-1)  # Negative values should raise a ValueError
    
    assert zero.value == 0
    assert one.value == 1

def test_successor():
    successor_of_two = two.successor()
    assert successor_of_two.value == 3
    assert one.successor().value == 2

def test_is_zero():
    # Test the is_zero method
    assert zero.is_zero() is True
    assert one.is_zero() is False
    assert two.is_zero() is False

def test_equality():
    # Test the equality method
    another_zero = NaturalNumber(0)
    another_two = one.successor()

    assert zero == another_zero
    assert zero != one
    assert two == another_two
    assert two != one

def test_add():
    # Test the add method
    result = one + two
    assert result.value == 3
    assert result == three

    result = two + one
    assert result.value == 3
    assert result == three

    result = one + one
    assert result.value == 2
    assert result == two

    result = zero + one
    assert result.value == 1
    assert result == one

def test_add_invalid():
    # Test adding invalid types
    with pytest.raises(ValueError):
        one + "kevin"
    with pytest.raises(ValueError):
        two + 5  # other value must be a natural number instance

def test_multiply():
    # Test the multiply method
    result = one * two
    assert result.value == 2
    assert result == two

    result = two * two
    assert result.value == 4
    assert result == four

    result = zero * two
    assert result.value == 0
    assert result == zero


def test_associativity():
    assert (two * three) * four == two * (three * four)

def test_commutativity():
    assert two * three == three * two

def test_left_distributivity():
    assert two * (three + four) == (two * three) + (two * four)

def test_right_distributivity():
    assert (three + four) * two == (three * two) + (four * two)
