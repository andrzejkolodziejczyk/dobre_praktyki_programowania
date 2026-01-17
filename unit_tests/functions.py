import re

def is_palindrome(text: str) -> bool:
    # Ignorowanie wielkości liter i spacji
    clean_text = "".join(text.lower().split())
    return clean_text == clean_text[::-1]

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def count_vowels(text: str) -> int:
    # Uwzględnienie polskich znaków (ą, ę, ó) zgodnie z przykładem "Próba żółwia"
    vowels = "aeiouyąęó"
    return sum(1 for char in text.lower() if char in vowels)

def calculate_discount(price: float, discount: float) -> float:
    if not (0 <= discount <= 1):
        raise ValueError("Discount must be between 0 and 1")
    return float(price * (1 - discount))

def flatten_list(nested_list: list) -> list:
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

def word_frequencies(text: str) -> dict:
    if not text:
        return {}
    # Usunięcie interpunkcji i podział na słowa
    words = re.findall(r'\b\w+\b', text.lower())
    frequencies = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True