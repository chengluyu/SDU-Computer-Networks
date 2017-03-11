from random import randint
from queue import Queue
from sys import argv
from simulation import Packet, Generator, Histogram


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
        self.lines = [Line(i) for i in range(queue_count)]
        self.line_with_minimal_arrival_time = None

    def next_arrival_line(self):
        return min(self.lines, key=lambda x: x.generator.next_arrival_time)

    def schedule(self):
        # return self.lines[randint(0, self.queue_count - 1)]
        return max(self.lines, key=lambda l: l.queue.qsize())

if __name__ == '__main__':
    total_packet_count = 1000000
    check_point_count = 100000
    default_queue_count = 3 if len(argv) == 1 else int(argv[1])

    simulated_packet_count = 0
    current_time = 0.0
    current_packet_finished_time = 0.0

    queues = MultipleQueue(default_queue_count)

    while simulated_packet_count < total_packet_count:
        # pick the line with minimal arrival time
        line = queues.next_arrival_line()

        if current_packet_finished_time < line.generator.next_arrival_time:
            simulated_packet_count += 1
            if simulated_packet_count % check_point_count == 0:
                print('Simulated %d packets' % simulated_packet_count)

            line = queues.schedule()

            if line.queue.empty():
                packet = line.generator.next()
                current_time = packet.arrival_time
                current_packet_finished_time = current_time + packet.service_time
                line.log_waiting_time(0.0)
            else:
                packet = line.queue.get(block=False)
                current_time = current_packet_finished_time
                current_packet_finished_time = current_time + packet.service_time
                line.log_waiting_time(current_time - packet.arrival_time)
        else:
            packet = line.generator.next()
            current_time = packet.arrival_time
            line.queue.put(packet)

    for line in queues.lines:
        Histogram.plot(line.waiting_time_samples)

    Histogram.show()
