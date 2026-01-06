import random

class SSH:
    def __init__(self):
        self.__port = random.randint(9000, 65535)
        