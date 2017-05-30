from multiprocessing import Pool


class Process:
    def __init__(self, processes=8):
        self.p = Pool(processes)

    def Exec(self, f, data):
        return self.p.map(f, data)
