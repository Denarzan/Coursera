"""Descriptor with commission"""


class Value:
    def __init__(self):
        self.value = 1

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value * (1 - instance.commission)

    def __del__(self):
        return self

