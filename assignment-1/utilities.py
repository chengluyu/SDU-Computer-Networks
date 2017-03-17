from random import expovariate, randint
from queue import Queue
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


class Line:
    def __init__(self, identity, generator=Generator()):
        self.id = identity
        self.queue = Queue()
        self.generator = Generator()
        self.waiting_time_samples = []

    def log_waiting_time(self, waiting_time):
        self.waiting_time_samples.append(waiting_time)


class MultipleQueue:
    def __init__(self, queue_count):
        if type(queue_count) == list:
            lambdas = queue_count
            queue_count = len(lambdas)

        self.queue_count = queue_count
        self.next_queue_index = 0
        self.lines = [Line(i) for i in range(queue_count)]
        self.line_with_minimal_arrival_time = None

    def next_arrival_line(self):
        return min(self.lines, key=lambda x: x.generator.next_arrival_time)


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
