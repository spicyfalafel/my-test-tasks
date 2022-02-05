import random


class RandomInputs:
    @staticmethod
    def random_int(min=0, max=10):
        return random.randint(min, max)

    @staticmethod
    def random_phone_number(length=11):
        phone = '+'
        for i in range(length):
            phone += str(RandomInputs.random_int(max=9))
        return phone
