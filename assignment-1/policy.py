from utilities import Packet, Generator
from random import randint
from queue import Queue

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

    def schedule(self):
        pass


class RoundRobin(MultipleQueue):
    def __init__(self, queue_count):
        MultipleQueue.__init__(self, queue_count)
        self.next_queue_index = 0

    def schedule(self):
        line = self.lines[self.next_queue_index]
        self.next_queue_index += 1
        if self.next_queue_index == self.queue_count:
            self.next_queue_index = 0
        return line
