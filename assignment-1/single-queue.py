from queue import Queue
from utilities import Packet, Generator, Histogram


if __name__ == '__main__':
    total_packet_count = 1000000
    check_point_count = 100000

    current_time = 0.0
    current_packet_finished_time = 0.0
    simulated_packet_count = 0

    queue = Queue()
    generator = Generator()

    waiting_time_samples = []

    while simulated_packet_count < total_packet_count:
        # current packet will be served before next packet arrives
        if current_packet_finished_time < generator.next_arrival_time:
            simulated_packet_count += 1
            if simulated_packet_count % check_point_count == 0:
                print('Simulated %d packets' % simulated_packet_count)

            # if queue is empty, pick next packet from generator
            if queue.empty():
                packet = generator.next()
                current_time = packet.arrival_time
                current_packet_finished_time = packet.service_time + current_time
                waiting_time_samples.append(0.0)
            # if queue is not empty, pick next packet from queue
            else:
                packet = queue.get(block=False)
                current_time = current_packet_finished_time
                current_packet_finished_time = packet.service_time + current_time
                waiting_time_samples.append(current_time - packet.arrival_time)
        # next packet will arrive before current packet is finished
        else:
            packet = generator.next()
            current_time = packet.arrival_time
            queue.put(packet)
    
    Histogram.plot(waiting_time_samples)
    Histogram.show()
