from random import randint
from queue import Queue
from utilities import Packet, Generator, Histogram
from optparse import OptionParser


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
    # configure option parser
    op = OptionParser(usage='%prog [TEST-SPECS]')
    op.add_option('-q', '--queue', dest='queue_count', action='store',
                  help='How many queues are used in simulation', default=3)
    op.add_option('-p', '--packet', dest='packet_count', action='store',
                  help='How many packet are generated in simulation',
                  default=100000)

    (options, args) = op.parse_args()

    total_packet_count = int(options.packet_count)
    default_queue_count = int(options.queue_count)

    five_percent_count = int(total_packet_count / 20)

    simulated_packet_count = 0
    current_time = 0.0
    current_packet_finished_time = 0.0

    queues = MultipleQueue(default_queue_count)

    while simulated_packet_count < total_packet_count:
        # pick the line with minimal arrival time
        line = queues.next_arrival_line()

        if current_packet_finished_time < line.generator.next_arrival_time:
            simulated_packet_count += 1
            if simulated_packet_count % five_percent_count == 0:
                proportion = 5 * int(simulated_packet_count / five_percent_count)
                print('Simulated %d%% packets' % proportion)

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

    print('Done')

    for line in queues.lines:
        Histogram.plot(line.waiting_time_samples)

    Histogram.show()
