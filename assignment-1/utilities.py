from random import expovariate
import matplotlib.pyplot as plt
import numpy as np


class Packet:
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time


class Generator:
    def __init__(self):
        self.next_arrival_time = 0.0 + expovariate(0.5)

    def next(self):
        pack = Packet(self.next_arrival_time, expovariate(0.65))
        self.next_arrival_time += expovariate(0.5)
        return pack


class Histogram:
    def __init__(self):
        pass

    @staticmethod
    def plot(data):
        counts, bins = np.histogram(data, bins=400, normed=True)
        counts = [sum(counts[i:]) for i in range(len(counts))]
        bins = (bins[:-1] + bins[1:]) / 2
        plt.plot(bins, counts)

    @staticmethod
    def show():
        plt.semilogy()
        plt.show()