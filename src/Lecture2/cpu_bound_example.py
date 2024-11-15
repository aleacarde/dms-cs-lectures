# Example of a CPU-bound operation in Python

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(1000))  # Calculating a large factorial is CPU-intensive