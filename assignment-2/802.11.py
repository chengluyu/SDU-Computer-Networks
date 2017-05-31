from Util import Analyzer, Plot, APlot
from QueueBase import Queue
from multiprocesser import Process
import random
import numpy


def main(slot=1.0, stc=1):
    LAMBDA = [15] * 5
    MU = 100
    TOTAL = 1e5
    CHECK = 1e4

    def l(x=None):
        count = sum([len(i) for i in QLlog])
        if x.get('type') == 'birth':
            if count <= TOTAL * snum:
                if count % CHECK == 0:
                    pass
                    # print('Simulated %d packets. (%.2f%%)' % (count, count / (TOTAL * snum) * 100))
                for i in iterator:
                    if len(QLlog[i]) >= TOTAL:
                        stations[i].stop()

    snum = len(LAMBDA)
    iterator = range(snum)
    stations = [Queue(LAMBDA[i], MU) for i in iterator]
    time_slot = slot / MU
    backoff = [0] * snum
    nthclsion = [0] * snum
    signal = [0] * snum
    QLlog = [[] for i in iterator]
    WTlog = [[] for i in iterator]
    time = 0
    collision = 0
    busy = 0
    use = 0
    idle = 0
    init(stations, QLlog, WTlog, l)
    update(stations, time)
    while sum([len(i) for i in QLlog]) < TOTAL * snum or sum([i.length() for i in stations]):
        for i in iterator:
            if (not backoff[i]) and (stations[i].head() is not None):
                signal[i] = 1
            else:
                signal[i] = 0
        if sum(signal) <= 0:
            time += 1
            idle += 1
            update(stations, time * time_slot)
            for i in iterator:
                backoff[i] -= min(1, backoff[i])
            continue
        elif sum(signal) > 1:
            collision += sum(signal)
            idle -= 1
            for i in iterator:
                if signal[i]:
                    if nthclsion[i] < 16:
                        nthclsion[i] += 1
                    nthclsion[i] = max(nthclsion[i], stc)
                    # backoff[i] = random.randint(0, 2 ** max(nthclsion[i], sum(signal) - 1) - 1)
                    backoff[i] = random.randint(1, 2 ** min(nthclsion[i], 10))
            continue
        for i in iterator:
            if signal[i]:
                nthclsion[i] = 0
                station = stations[i]
                busy += station.head().size
                tmp = int(max(numpy.ceil(station.head().size / time_slot), 1))
                station.death()
                tmp = int(max(tmp, numpy.ceil(station.time() / time_slot - time)))
                time += tmp
                use += tmp
                update(stations, time * time_slot)
                for j in iterator:
                    backoff[j] -= min(tmp, backoff[j])
                break
    # print('Processing data...')
    # for i in QLlog:
    #     i.sort()
    # for i in WTlog:
    #     i.sort()
    # QLFin = [Analyzer.parse(i) for i in QLlog]
    # WTFin = [Analyzer.parse(i) for i in WTlog]
    # plt = Plot(QLFin, WTFin)
    CP = collision / (collision + TOTAL * snum) * 100
    EF = busy / time_slot / time * 100
    TP = use / time * 100
    # MQL = sum([sum(i) for i in QLlog]) / TOTAL / snum
    MWT = sum([sum(i) for i in WTlog]) / TOTAL / snum
    # print('Collision Probability: %.3f%%' % CP)
    # print('Occupancy rate of channel: %.3f%%' % OR)
    # print('Throughput: %.3f%%' % TP)
    # print('Done!')
    # plt.show()
    return (time_slot, CP, EF, TP, MWT)


def init(stations, QLlog, WTlog, log=None):
    def bind(s, q, w):
        s.on('birth', lambda x: (q.append(x.get('data')), log(x)))
        s.on('death', lambda x: (w.append(x.get('data')), log(x)))

    if log is None:
        log = lambda x: None

    for i in range(len(stations)):
        bind(stations[i], QLlog[i], WTlog[i])


def update(stations, time):
    for st in stations:
        st.wait(time)


if __name__ == '__main__':
    p = Process(8)
    fin = p.Exec(main, [0.01 * i + 0.3 for i in range(170)])
    # print(fin)
    plt = APlot(fin)
    plt.show()
    # main(0.625)
