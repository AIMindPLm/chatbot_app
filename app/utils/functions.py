# utils/functions.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Division by zero is not allowed."

def is_even_or_odd(number: int) -> str:
    if number % 2 == 0:
        return f"The number {number} is even."
    else:
        return f"The number {number} is odd."
