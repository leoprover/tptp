import time

class Timer:
    def __init__(self):
        self.scheduledTime = None
        self.startTime = None
        self.endTime = None

    def schedule(self):
        if self.scheduledTime is not None:
            raise Exception(self.scheduledTime)
        if self.startTime is not None:
            raise Exception(self.startTime)
        if self.endTime is not None:
            raise Exception(self.endTime)
        self.scheduledTime = time.time()

    def start(self):
        if self.scheduledTime is None:
            raise Exception(self.scheduledTime)
        if self.startTime is not None:
            raise Exception(self.startTime)
        if self.endTime is not None:
            raise Exception(self.endTime)
        self.startTime = time.time()

    def end(self):
        if self.scheduledTime is None:
            raise Exception(self.scheduledTime)
        if self.startTime is None:
            raise Exception(self.startTime)
        if self.endTime is not None:
            raise Exception(self.endTime)
        self.endTime = time.time()

    def getScheduled(self, zero = 0):
        if self.scheduledTime is None:
            return None
        return self.scheduledTime - zero

    def getStart(self, zero = 0):
        if self.startTime is None:
            return None
        return self.startTime - zero

    def getEnd(self, zero = 0):
        if self.endTime is None:
            return None
        return self.endTime - zero

    def getTimeScheduled(self):
        if self.scheduledTime is None:
            return 0
        if self.startTime is None:
            return time.time() - self.scheduledTime
        return self.startTime - self.scheduledTime

    def getTimeRunning(self):
        if self.endTime:
            if self.startTime is None:
                raise Exception(self.startTime)
            return self.endTime - self.startTime
        if self.startTime:
            return time.time() - self.startTime
        return 0

    def __str__(self):
        if self.scheduledTime is None:
            return 'Not yet scheduled'
        if self.startTime is None:
            return 'scheduled {}s ago'.format(time.time() - self.scheduledTime)
        elif self.endTime is None:
            return '{}s scheduled, started {}s ago'.format(self.startTime - self.scheduledTime, time.time() - self.startTime)
        else:
            return '{}s scheduled, {}s runned'.format(self.startTime - self.scheduledTime, self.endTime - self.startTime)

class CountdownTimer:
    def __init__(self, timeout):
        '''
        timeout in s
        '''
        self.timeout = timeout
        self.startTime = time.time()

    def timeleft(self):
        return self.timeout - (time.time() - self.startTime)

    def getStart(self, zero = 0):
        if self.startTime is None:
            return None
        return self.startTime - zero
    