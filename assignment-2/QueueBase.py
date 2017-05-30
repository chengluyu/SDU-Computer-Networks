from PacketBase import Packet
from typing import Callable
from numpy import random
import queue as Q
import sys


class Queue:
    def __init__(self, lmd: float, mu: float):
        if lmd <= 0:
            raise Exception('Lambda cannot less than 0')
        if mu <= 0:
            raise Exception('Mu cannot less than 0')
        self.lmd = lmd
        self.mu = mu
        self.processTime = 0
        self.offsetTime = 0
        self.nextBirthTime = 0
        self.nextDeathTime = sys.maxsize
        self.birthListener = []
        self.deathListener = []
        self.queue = Q.Queue()
        self.curPacket = None

    def next(self):
        if self.nextBirthTime - self.offsetTime <= self.nextDeathTime:
            data = self.__BirthHandler__()
            data = {
                'type': 'birth',
                'data': data
            }
            for bk in self.birthListener:
                bk(data)
            return data
        else:
            data = self.__DeathHandler__()
            data = {
                'type': 'death',
                'data': data
            }
            for bk in self.deathListener:
                bk(data)
            return data

    def birth(self):
        res = {}
        while res.get('type') != 'birth':
            res = self.next()
        return res

    def death(self):
        res = {}
        while res.get('type') != 'death':
            res = self.next()
        return res

    def wait(self, time: float):
        if time < self.processTime + self.offsetTime:
            raise Exception('The time cannot less than the current time')
        self.offsetTime = time - self.processTime
        while self.nextBirthTime <= time:
            self.birth()

    def length(self):
        if self.curPacket:
            return self.queue.qsize() + 1
        else:
            return self.queue.qsize()

    def head(self):
        if not self.curPacket:
            try:
                self.curPacket = self.queue.get(block=False)
            except Q.Empty:
                self.curPacket = None
        return self.curPacket

    def time(self):
        return self.processTime + self.offsetTime

    def stop(self):
        self.nextBirthTime = sys.maxsize

    def on(self, tp: str, callback: Callable[[object], None]):
        if tp == 'birth':
            self.birthListener.append(callback)
        elif tp == 'death':
            self.deathListener.append(callback)

    def __BirthHandler__(self):
        packet = Packet(self.mu)
        packet.arriveTime = self.nextBirthTime
        self.queue.put(packet, block=False)
        if self.processTime < self.nextBirthTime - self.offsetTime:
            self.processTime = self.nextBirthTime - self.offsetTime
        self.nextBirthTime += random.exponential(1 / self.lmd)
        if self.length() == 1:
            self.nextDeathTime = self.processTime
        return self.length()

    def __DeathHandler__(self):
        packet = self.head()
        waitTime = self.time() - packet.arriveTime
        self.processTime = self.nextDeathTime + packet.size
        self.curPacket = None
        if self.length() == 0:
            self.nextDeathTime = sys.maxsize
        else:
            self.nextDeathTime = self.processTime
        return waitTime
