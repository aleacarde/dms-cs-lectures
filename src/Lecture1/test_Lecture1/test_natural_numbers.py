import pytest

from src.Lecture1.Lecture1 import NaturalNumber, NaturalNumbers


def setup_function():
    global naturals
    naturals = NaturalNumbers()

def test_getitem_valid_index():
    # Test accessing elements by index
    assert naturals[0].value == 0
    assert naturals[1].value == 1
    assert naturals[5].value == 5
    assert naturals[100].value == 100  # Test large index access
    assert naturals[10].value == 10  # Ensure caching works for previously accessed indices

def test_getitem_negative_index():
    # Test accessing a negative index raises an IndexError
    with pytest.raises(IndexError):
        naturals[-1]

def test_iteration():
    # Test iterating over the first 10 natural numbers
    from itertools import islice
    values = [n.value for n in islice(naturals, 10)]
    assert values == list(range(10))

def test_caching():
    # Test that values are cached correctly
    assert 0 in naturals.cache
    assert naturals[50].value == 50  # This should trigger caching up to index 50
    assert all(i in naturals.cache for i in range(51))  # Ensure all values up to 50 are cached

def test_large_index_access():
    # Test accessing a very large index
    large_index = 10000
    assert naturals[large_index].value == large_index

def test_lazy_evaluation():
    # Test that numbers are generated on demand
    iterator = iter(naturals)
    assert next(iterator).value == 0
    assert next(iterator).value == 1
    assert next(iterator).value == 2
    assert 3 not in naturals.cache  # The generator does not automatically cache during iteration

def test_type_of_generated_numbers():
    # Ensure that generated numbers are instances of NaturalNumber
    assert isinstance(naturals[0], NaturalNumber)
    assert isinstance(naturals[5], NaturalNumber)
    assert isinstance(next(iter(naturals)), NaturalNumber)