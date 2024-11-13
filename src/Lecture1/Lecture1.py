# Peano Axioms
from typing import Self, Generator


class NaturalNumber:
    def __init__(self, value=0) -> Self:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Natural numbers must be non-negative integers.")
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def successor(self) -> Self:
        """
        Returns the successor of the current natural number.
        Note: This is technically cheating, but it gets the point across.
        """
        return NaturalNumber(self.value + 1)
    
    def is_zero(self) -> bool:
        """Returns true if the natural number is zero."""
        return self.value == 0

    def is_positive(self) -> bool:
        """Returns true if the natural number is greater than zero."""
        return not self.is_zero()
    
    def predecessor(self) -> Self:
        """
        Returns the predecessor of a positive natural number.
        Raises a value error if the number is not positive.
        Note: Like the successor function, this is also technically cheating but it gets the point across.
        """
        if not self.is_positive():
            raise ValueError("Zero is not the successor of any natural number.")
        return NaturalNumber(self.value - 1)
    
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, NaturalNumber):
            return False
        return self.value == other.value
    
    def __add__(self, other: Self) -> Self:
        """Adds two natural numbers recursively using the successor method."""
        if not isinstance(other, NaturalNumber):
            raise ValueError("Can only add another natural number.")
        
        if self.is_zero():
            return other

        return (self.predecessor() + other).successor()
    
    def __mul__(self, other: Self) -> Self:
        """Adds two natural numbers recursively using the successor method."""
        if not isinstance(other, NaturalNumber):
            raise ValueError("Can only multiply another natural number.")
        
        if self.is_zero():
            return NaturalNumber(0)
        
        return (self.predecessor() * other) + other


class LessEfficientNaturalNumbers:
    def __init__(self):
        self.cache = [NaturalNumber(0)]  # Start with the first natural number (0)

    def __getitem__(self, index):
        # If the requested index is greater than the cache length, generate new numbers
        while len(self.cache) <= index:
            last_number = self.cache[-1]
            self.cache.append(last_number.successor())
        return self.cache[index]

    def __iter__(self) -> Generator[Self, None, None]:
        index = 0
        while True:
            # Yield numbers, using __getitem__ to leverage caching
            yield self[index]
            index += 1


class NaturalNumbers:
    def __init__(self):
        self.cache = {0: NaturalNumber(0)}  # Start with the first natural number (0)

    def __getitem__(self, index):
        if index < 0:
            raise IndexError("Index must be a non-negative integer")
        # Generate and cache numbers up to the requested index, if not already cached
        if index not in self.cache:
            # Start from the last cached index to minimize redundant generation
            last_index = max(self.cache)
            last_number = self.cache[last_index]
            for i in range(last_index + 1, index + 1):
                self.cache[i] = last_number.successor()
                last_number = self.cache[i]
        return self.cache[index]

    def __iter__(self):
        index = 0
        while True:
            yield self[index]
            index += 1

natural_numbers = NaturalNumbers()
