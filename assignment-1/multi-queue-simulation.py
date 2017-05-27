from collections import deque
from datetime import datetime
from random import expovariate, choice
from string import ascii_uppercase, digits
from progressbar import ProgressBar
from matplotlib import pyplot as plt
from numpy import histogram
from scipy.interpolate import UnivariateSpline

def random_string(length):
    return ''.join(choice(ascii_uppercase + digits) for _ in range(length))

class Packet:
    def __init__(self, arrival_time, service_time, queue_index):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.queue_index = queue_index
        # self.name = random_string(8) # for debug use only

class Queue:
    def __init__(self):
        self.data = deque()
        self.peep = None

    def peek(self):
        if self.peep is None:
            self.peep = self.data.popleft()
            return self.peep
        else:
            return self.peep

    def length(self):
        return len(self.data)

    def empty(self):
        return len(self.data) == 0

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if self.peep is None:
            return self.data.popleft()
        else:
            ret, self.peep = self.peep, None
            return ret

# a scheduler function should returns a queue to be served,
# or returns None if no queues can be served

# choose a queue from non-empty queues randomly
def randomized_schedule(waiting_queues):
    while True:
        nonempty_queues = list(filter(lambda q: not q.empty(), waiting_queues))
        yield choice(nonempty_queues) if len(nonempty_queues) > 0 else None

# classic round robin method
def round_robin(waiting_queues):
    # a counter that prevents scheduler from infinite loop
    counter = 0
    while True:
        for queue in waiting_queues:
            if queue.empty():
                counter += 1
                if counter == len(waiting_queues):
                    yield None
                    counter = 0 # reset the counter
                continue
            else:
                yield queue
                counter = 0 # reset the counter

def deficit_round_robin(waiting_queues, quantums):
    deficit_counters = [ 0 ] * len(waiting_queues)

    # a counter that prevents scheduler from infinite loop
    empty_counter = 0

    while True:
        for (index, queue) in enumerate(waiting_queues):
            deficit_counters[index] += quantums[index]
            while not queue.empty() and deficit_counters[index] >= queue.peek().service_time:
                deficit_counters[index] -= queue.peek().service_time
                yield queue
                empty_counter = 0 # reser the counter
            else:
                empty_counter += 1
                if empty_counter == len(waiting_queues):
                    yield None
                    empty_counter = 0 # reset the counter
            if queue.empty():
                deficit_counters[index] = 0


if __name__ == '__main__':
    # limits
    queue_count = 3
    total_packet_count = 10 ** 6

    # parameters
    arrival_lambds = [0.8, 0.5, 0.3]
    service_lambd = 1.65

    # for prompt use only
    progress_bar = ProgressBar(max_value=total_packet_count, redirect_stdout=True)

    # performance measurements
    server_total_busy_time = 0.0

    # records for each queue
    waiting_time_records = [ [] for _ in range(queue_count) ]
    queue_length_records = [ [] for _ in range(queue_count) ]

    # state variables
    served_packet_count = 0
    current_time = 0.0
    server_is_idle = True
    current_job_finish_time = 0.0
    current_job = None

    # objects
    next_arrival_times = [ expovariate(lambd) for lambd in arrival_lambds ]
    waiting_queues = [Queue() for _ in range(queue_count)]

    # the scheduler
    # scheduler = round_robin(waiting_queues)
    scheduler = deficit_round_robin(waiting_queues, [80, 60, 45])

    while served_packet_count < total_packet_count:
        index, time = min(enumerate(next_arrival_times), key=lambda t: t[1])
        if server_is_idle or time < current_job_finish_time:
            current_time = time
            packet = Packet(time, expovariate(service_lambd), index)
            next_arrival_times[index] += expovariate(arrival_lambds[index])
            waiting_queues[index].push(packet)
            queue_length_records[index].append(waiting_queues[index].length())
        else:
            current_time = current_job_finish_time
            server_is_idle = True
            served_packet_count += 1
            server_total_busy_time += current_job.service_time
            progress_bar.update(served_packet_count)

        if server_is_idle:
            selected_queue = next(scheduler)
            if selected_queue is not None:
                packet = selected_queue.pop()
                waiting_time_records[packet.queue_index].append(current_time - packet.arrival_time)
                server_is_idle = False
                current_job = packet
                current_job_finish_time = current_time + current_job.service_time

    progress_bar.finish()

    # create two sub-plots
    fig, (left, right) = plt.subplots(1, 2)
    fig.set_size_inches(12, 7)

    # waiting time distributions
    for (i, waiting_times) in enumerate(waiting_time_records):
        counts, bin_edges = histogram(waiting_times, bins=100, density=True)
        cdf = [sum(counts[i:]) * (bin_edges[1] - bin_edges[0]) for i in range(len(counts))]
        bins_avg = (bin_edges[:-1] + bin_edges[1:]) / 2
        left.plot(bins_avg, cdf, label='Queue #%d (lambda=%.2f)' % (i, arrival_lambds[i]))

    left.set_title('Waiting Time')
    left.legend(loc='upper right', shadow=True, fontsize='small')
    left.set_xlabel('Time Unit')
    left.set_ylabel('Probability')
    left.semilogy()

    # queue length distributions
    for (i, queue_lengths) in enumerate(queue_length_records):
        counts, bin_edges = histogram(queue_lengths, bins=100, density=True)
        cdf = [sum(counts[i:]) * (bin_edges[1] - bin_edges[0]) for i in range(len(counts))]
        bins_avg = (bin_edges[:-1] + bin_edges[1:]) / 2

        right.plot(bins_avg, cdf, label='Queue #%d (lambda=%.2f)' % (i, arrival_lambds[i]))

    right.set_title('Queue Length')
    right.legend(loc='upper right', shadow=True, fontsize='small')
    right.set_xlabel('Size')
    right.set_ylabel('Probability')
    right.semilogy()

    # main title
    server_busy_percentage = 100 * server_total_busy_time / current_time
    plt.suptitle('Cumulative Distribution (Busy Time: %f%%)' % server_busy_percentage)

    # it's show time!
    plt.show()

    # save the figure
    fig.savefig('fig-' + datetime.now().strftime('%b-%d-%H-%M-%S') + '.png')
