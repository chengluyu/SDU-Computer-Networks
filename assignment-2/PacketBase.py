from numpy import random


class Packet:
    def __init__(self, lmd: float):
        if lmd <= 0:
            raise Exception("Lambda cannot less than 0")
        self.arriveTime = 0
        self.size = random.exponential(1 / lmd)
