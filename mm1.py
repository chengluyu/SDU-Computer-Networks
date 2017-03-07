from random import expovariate
from queue import Queue

class Packet:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.serving_time = expovariate(0.65)

class Queue:
    def __init__(self):
        self.queue = Queue()
    
    def generate(self):
        self.queue.
        

if __name__ == '__main__':
    total_packet_count = 10000000

    queue = Queue()
    current_time = 0.0
    served_packet_count = 0

    the_packet = None

    while served_packet_count < total_packet_count:
        if the_packet is None:
            if queue.empty():
                current_time += expovariate(0.5)
                the_packet = Packet(current_time)
            else:
                the_packet = queue.get()
        else:
            current_time += the_packet.serving_time
            the_packet = None
            

        