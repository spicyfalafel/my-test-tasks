import random
import string


class StringUtils:
    @staticmethod
    def generate_random(min=1, max=10, uppercase=True, special=False, with_symbols=""):
        symbols = string.digits + string.ascii_lowercase
        symbols = symbols + string.ascii_uppercase if uppercase else symbols
        spec = ['!', '_', '?']
        symbols = symbols + spec if special else symbols

        num = random.choice(range(min, max + 1))
        symbols_to_add = len(with_symbols)
        return ''.join([random.choice(symbols) for _ in range(num-symbols_to_add)]).join(list(symbols))

    @staticmethod
    def contains_upper(str):
        return any(ch.isupper() for ch in str)

    @staticmethod
    def contains_digit(str):
        return any(ch.isdigit() for ch in str)



