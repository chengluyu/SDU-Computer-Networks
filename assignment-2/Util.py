from matplotlib import pyplot as plt
import numpy


class Plot:
    def __init__(self, ql=None, wt=None):
        figure = 0
        if ql is not None:
            figure += 1
        if wt is not None:
            figure += 1
        plt.figure(1)
        if not figure:
            return
        if figure == 1:
            if ql is not None:
                title = 'Queue Length Cumulative Distribution'
                obj = ql
                xlabel = 'Queue Length'
            else:
                title = 'Waiting Time Cumulative Distribution'
                obj = wt
                xlabel = 'Waiting Time'
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel('Probability')
            plt.semilogy()
            for i, j in obj:
                plt.plot(i, j)
        else:
            plt.subplot(121)
            for i, j in ql:
                plt.plot(i, j)
            plt.title('Queue Length Cumulative Distribution')
            plt.xlabel('Queue Length')
            plt.ylabel('Probability')
            plt.semilogy()
            plt.subplot(122)
            for i, j in wt:
                plt.plot(i, j)
            plt.title('Waiting Time Cumulative Distribution')
            plt.xlabel('Waiting Time')
            plt.ylabel('Probability')
            plt.semilogy()

    @staticmethod
    def show():
        plt.show()


class Analyzer:
    def __init__(self):
        pass

    @staticmethod
    def parse(arr, bins=1000):
        counts, bi = numpy.histogram(arr, bins=bins, density=True)
        pct = [sum(counts[i:]) * (bi[1] - bi[0]) for i in range(len(counts))]
        avg = (bi[:-1] + bi[1:]) / 2
        return avg, pct


class APlot:
    def __init__(self, data=None):
        plt.figure(1)
        plt.subplot(221)
        TP = []
        IP = []
        JP = []
        KP = []
        LP = []
        for t, i, j, k, l in data:
            TP.append(t)
            IP.append(i)
            JP.append(j)
            KP.append(k)
            LP.append(l)
        plt.title('Collision Probability Distribution')
        plt.xlabel('Time Slot Length')
        plt.ylabel('Probability')
        plt.plot(TP, IP)
        plt.subplot(222)
        plt.title('Occupancy rate of channel Distribution')
        plt.xlabel('Time Slot Length')
        plt.ylabel('Occupancy rate')
        plt.plot(TP, JP)
        plt.subplot(223)
        plt.title('Throughput Distribution')
        plt.xlabel('Time Slot Length')
        plt.ylabel('Throughput')
        plt.plot(TP, KP)
        plt.subplot(224)
        plt.title('Mean Waiting Time Distribution')
        plt.xlabel('Time Slot Length')
        plt.ylabel('Waiting Time')
        plt.plot(TP, LP)

    @staticmethod
    def show():
        plt.show()
        plt.savefig("2333.eps")
