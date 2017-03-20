from utilities import Histogram, MultipleQueue
from optparse import OptionParser
from policy import Policy


if __name__ == '__main__':
    # configure option parser
    op = OptionParser(usage='%prog [TEST-SPECS]')
    op.add_option('-q', '--queue', dest='queue_count', action='store',
                  help='How many queues are used in simulation', default=3)
    op.add_option('-c', '--count', dest='packet_count', action='store',
                  help='How many packet are generated in simulation',
                  default=100000)
    op.add_option('-p', '--policy', dest='policy_name', action='store',
                  help='Specify the strategy', default='roundrobin')

    (options, args) = op.parse_args()

    total_packet_count = int(options.packet_count)
    queue_count = int(options.queue_count)
    policy_name = options.policy_name

    print('''Simulation info:
    packet count = %d
    queue count = %d
    policy name = %s''' % (total_packet_count, queue_count, policy_name))

    five_percent_count = int(total_packet_count / 20)

    simulated_packet_count = 0
    current_time = 0.0
    current_packet_finished_time = 0.0

    queues = MultipleQueue(queue_count)
    policy = Policy.get_by_name(name=options.policy_name, queues=queues)

    while simulated_packet_count < total_packet_count:
        # pick the line with minimal arrival time
        line = queues.next_arrival_line()

        if current_packet_finished_time < line.generator.next_arrival_time:
            simulated_packet_count += 1
            if simulated_packet_count % five_percent_count == 0:
                proportion = 5 * int(simulated_packet_count / five_percent_count)
                print('Simulated %d%% packets' % proportion)

            line = policy.schedule(current_time)

            if line.queue.empty():
                packet = line.generator.next()
                current_time = packet.arrival_time
                current_packet_finished_time = current_time + packet.service_time
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
