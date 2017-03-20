from utilities import MultipleQueue
from random import randint

class Policy:
    def __init__(self, queues: MultipleQueue):
        self.queues = queues

    def schedule(self, current_time: float):
        pass

    @staticmethod
    def get_by_name(name, queues: MultipleQueue):
        policies = {
            'roundrobin': RoundRobin,
            'random': Randomized
        }
        return policies[name](queues)


class RoundRobin(Policy):
    def __init__(self, queues: MultipleQueue):
        Policy.__init__(self, queues)
        self.next_queue_index = 0

    def schedule(self, current_time: float):
        line = self.queues.lines[self.next_queue_index]
        self.next_queue_index += 1
        if self.next_queue_index == self.queues.queue_count:
            self.next_queue_index = 0
        return line


class Randomized(Policy):
    def __init__(self, queues: MultipleQueue):
        Policy.__init__(self, queues)

    def schedule(self, current_time: float):
        lines = self.queues.lines
        return lines[randint(0, len(lines) - 1)]

class ExponentialBackoff(Policy):
    def __init__(self, queues: MultipleQueue):
        Policy.__init__(self, queues)

    def schedule(self, current_time: float):
        pass
