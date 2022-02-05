import random


class RandomInputs:
    @staticmethod
    def random_number(min=0, max=10):
        return random.randint(min, max)
