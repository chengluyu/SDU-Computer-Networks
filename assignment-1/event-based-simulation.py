from queue import Queue
from heapq import heappush, heappop
from random import expovariate, choice
from string import ascii_uppercase, digits
from utilities import Histogram

class Packet:
    def __init__(self, arrival_time, service_time, name = ''):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.name = name

class PacketQueue:
    def __init__(self):
        self.queue = Queue()
        self.peep = None

    def empty(self):
        return self.queue.empty()

    def peek(self):
        if self.peep is None:
            self.peep = self.queue.get(block=False)
            return self.peep
        else:
            return self.peep

    def push(self, packet):
        self.queue.put(packet)

    def pop(self):
        if self.peep is None:
            return self.queue.get(block=False)
        else:
            result = self.peep
            self.peep = None
            return result

class Event:
    KIND_ARRIVAL = 0
    KIND_FINISHED = 1

    def __init__(self, kind, time, queue_number, packet):
        self.kind = kind
        self.time = time
        self.queue_index = queue_number
        self.packet = packet

class EventQueue:
    def __init__(self):
        self.queue = []

    def push(self, item):
        heappush(self.queue, item)

    def schedule_arrival(self, queue_index, packet):
        item = (packet.arrival_time, Event.KIND_ARRIVAL, queue_index, packet)
        self.push(item)

    def schedule_finished(self, time, queue_number, packet):
        item = (time, Event.KIND_FINISHED, queue_number, packet)
        self.push(item)

    def pop(self):
        (time, kind, queue_number, packet) = heappop(self.queue)
        return Event(kind, time, queue_number, packet)

class Generator:
    def __init__(self, arrival_lambda, service_lambda):
        self.last_time = 0.0
        self.arrival_lambda = arrival_lambda
        self.service_lambda = service_lambda

    def next(self):
        name = ''.join(choice(ascii_uppercase + digits) for _ in range(6))
        self.last_time = self.last_time + expovariate(self.arrival_lambda)
        return Packet(self.last_time, expovariate(self.service_lambda), name)

def roundRobin(queues):
    while True:
        # this will always be true if all queues are empty
        scheduled = False

        for (i, q) in enumerate(queues):
            if not q.empty():
                yield (i, q.pop())
                scheduled = True

        # check if all queues are empty
        if not scheduled:
            yield (None, None)

def deficitRoundRobin(queues, quantum):
    dc = [0 for _ in queues]
    q = quantum

    while True:
        # this will always be true if all queues are empty
        scheduled = False

        for (i, queue) in enumerate(queues):
            if not queue.empty():
                dc[i] = dc[i] + q[i]
                while (not queue.empty()) and (dc[i] >= queue.peek().service_time):
                    dc[i] = dc[i] - queue.peek().service_time
                    yield (i, queue.pop())
                if queue.empty():
                    dc[i] = 0

        # check if all queues are empty
        if not scheduled:
            yield (None, None)

if __name__ == '__main__':
    total_packet_count = 10000
    five_percent_count = int(total_packet_count / 20)
    total_queue_count = 3
    queue_arrival_lambdas = [0.3, 0.2, 0.1]
    queue_service_lambdas = [0.65] * 3

    # for debug use
    loop_counter = 0

    current_time = 0.0
    served_packet_count = 0
    server_is_busy = False
    waiting_times_records = [[] for _ in range(total_queue_count)]
    queues = [PacketQueue() for _ in range(total_queue_count)]
    generators = [Generator(queue_arrival_lambdas[i], queue_service_lambdas[i]) for i in range(total_queue_count)]
    event_queue = EventQueue()
    scheduler = deficitRoundRobin(queues, list(map(lambda x: 1 / x, queue_arrival_lambdas)))
    # scheduler = roundRobin(queues)

    # initialization
    for i in range(total_queue_count):
        event_queue.schedule_arrival(i, generators[i].next())

    while served_packet_count < total_packet_count:
        # verbose
        print("[%d]" % loop_counter, end='\n')
        loop_counter += 1

        event = event_queue.pop()
        assert current_time <= event.time
        current_time = event.time # sync time

        if event.kind == Event.KIND_ARRIVAL:
            # verbose
            print("ARRIVAL(#%d): name = %s, time = %fs" % (event.queue_index, event.packet.name, current_time))

            # push the arrival packet into its queue
            queues[event.queue_index].push(event.packet)

            # schedule the arrival event of next packet
            next_packet = generators[event.queue_index].next()
            event_queue.schedule_arrival(event.queue_index, next_packet)
        elif event.kind == Event.KIND_FINISHED:
            # verbose
            print("FINISH(#%d): name = %s, time = %fs" % (event.queue_index, event.packet.name, current_time))

            # set server free
            server_is_busy = False

            # increase counter
            served_packet_count = served_packet_count + 1

            if served_packet_count % five_percent_count == 0:
                proportion = 5 * int(served_packet_count / five_percent_count)
                print('Simulated %d%% packets' % proportion)
        else:
            raise Exception() # this will never happen

        if not server_is_busy:
            (queue_index, packet) = next(scheduler)
            if packet is None:
                continue

            print("SERVE(#%d): name = %s, interval = %fs, wait = %f, estimate = %fs" % (queue_index, packet.name, packet.service_time, current_time + packet.service_time - packet.arrival_time, current_time + packet.service_time))
            event_queue.schedule_finished(current_time + packet.service_time, queue_index, packet)
            waiting_times_records[event.queue_index].append(current_time + packet.service_time - packet.arrival_time)
            server_is_busy = True

    for waiting_times in waiting_times_records:
        Histogram.plot(waiting_times)

    Histogram.show()
