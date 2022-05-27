import threading
import time
import numpy

class FlopsTestThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loopCount = 0.0
        self.shutOff = False

    def exit(self):
        self.shutOff = True
        return self.loopCount

    def run(self):
        while not self.shutOff:
            self.loopCount += 1.0


class IopsTestThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loopCount = 0
        self.shutOff = False

    def exit(self):
        self.shutOff = True
        return self.loopCount

    def run(self):
        while not self.shutOff:
            self.loopCount += 1


class timerThread(threading.Thread):
    def __init__(self, timeToRun, testThreads):
        threading.Thread.__init__(self)
        self.timeToRun = timeToRun
        self.testThreads = testThreads
        self.ops = 0
        self.sum = 0
        self.val = 0
        self.avg = 0

    def getOps(self):
        return self.ops

    def run(self):
        time.sleep(self.timeToRun)
        for i in range(len(self.testThreads)):
            self.val = self.testThreads[i].exit()
            self.sum += self.val
        self.avg = self.sum * 2 / len(self.testThreads)
        # mult by 2 because loop check AND increment is done every loop. 2 operations
        self.ops = self.avg / self.timeToRun


def floatTest(numThreads, timeToRun, numRuns):
    timerThreads = []
    opsSum = 0
    print("running float operations test ...")
    for y in range(numRuns):
        testThreads = []
        for x in range(numThreads):
            testThreads.append(FlopsTestThread())
            testThreads[x].start()
        timerThreads.append(timerThread(timeToRun, testThreads))
        timerThreads[y].start()
        timerThreads[y].join()
    devList = []
    for z in range(len(timerThreads)):
        opsSum += timerThreads[z].getOps()
        devList.append(timerThreads[z].getOps() / 10**9)
    opsAvg = opsSum / len(timerThreads)
    stdDev = numpy.std(devList)
    print("average Giga Flops: ", opsAvg / 10**9, "with a deviation of: ", stdDev)


def iopsTest(numThreads, timeToRun, numRuns):
    timerThreads = []
    opsSum = 0
    print("running integer operations test ...")
    for y in range(numRuns):
        testThreads = []
        for x in range(numThreads):
            testThreads.append(IopsTestThread())
            testThreads[x].start()
        timerThreads.append(timerThread(timeToRun, testThreads))
        timerThreads[y].start()
        timerThreads[y].join()
    devList = []
    for z in range(len(timerThreads)):
        opsSum += timerThreads[z].getOps()
        devList.append(timerThreads[z].getOps() / 10**9)
    opsAvg = opsSum / len(timerThreads)
    stdDev = numpy.std(devList)
    print("average Giga Iops: ", opsAvg / 10**9, "with a deviation of: ", stdDev)


for x in range(1, 9):
    numThreads = x
    timeToRun = 10
    numRuns = 3
    print("testing with", numThreads, "threads and using a test time of", timeToRun, "seconds")
    floatTest(numThreads, timeToRun, numRuns)
    iopsTest(numThreads, timeToRun, numRuns)
    print("---------------------------")
