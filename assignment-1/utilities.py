from random import expovariate
import matplotlib.pyplot as plt
import numpy as np


class Packet:
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time


class Generator:
    def __init__(self, arrival_lambda=0.3, service_lambda=1.4):
        self.arrival_lambda = arrival_lambda
        self.service_lambda = service_lambda
        self.next_arrival_time = 0.0 + expovariate(arrival_lambda)

    def next(self):
        pack = Packet(self.next_arrival_time, expovariate(self.service_lambda))
        self.next_arrival_time += expovariate(self.arrival_lambda)
        return pack


class Histogram:
    def __init__(self):
        pass

    @staticmethod
    def plot(data):
        counts, bin_edges = np.histogram(data, bins=100, density=True)
        cdf = [sum(counts[i:]) for i in range(len(counts))]
        bins_avg = (bin_edges[:-1] + bin_edges[1:]) / 2
        plt.plot(bins_avg, cdf)

    @staticmethod
    def show():
        plt.title('Waiting Time Cumulative Distribution')
        plt.xlabel('Time Epoch')
        plt.ylabel('Probability')
        plt.semilogy()
        plt.show()
