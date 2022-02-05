import random
import string


def random_strings(times=1, min=1, max=10, uppercase=True, special=False, with_symbols=""):
    return [random_string(min, max, uppercase, special, with_symbols) for _ in range(times)]


def random_string(minim=1, maxim=10, uppercase=True, special=False, with_symbols=""):
    symbols = string.digits + string.ascii_lowercase
    symbols = symbols + string.ascii_uppercase if uppercase else symbols
    spec = '!_?'
    symbols = symbols + spec if special else symbols

    num = random.choice(range(minim, maxim + 1))
    symbols_to_add = len(with_symbols)
    return ''.join([random.choice(symbols) for _ in range(num - symbols_to_add)]) + ''.join(list(with_symbols))


def contains_upper(text):
    return any(ch.isupper() for ch in text)


def contains_digit(text):
    return any(ch.isdigit() for ch in text)
