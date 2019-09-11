class NotYetStartedError(Exception):
    pass

class Process:
    def isStarted(self) -> bool:
        """
        Whether to process has already been started.
        """
        raise NotImplementedError()

    def isRunning(self) -> bool:
        """
        Whether the process is currently running.
        """
        raise NotImplementedError()

    def isDone(self) -> bool:
        """
        Whether the process is done with execution.
        """
        raise NotImplementedError()

    def isTimeout(self) -> bool:
        """
        Whether the process was killed by an external timeout.
        """
        raise NotImplementedError()

    def isInterupted(self) -> bool:
        """
        Whether the process has beed tried to be canceled, terminated or killed.
        """
        raise NotImplementedError()

    def isCanceled(self) -> bool:
        """
        Whether the process has beed canceled.
        """
        raise NotImplementedError

    def isTerminated(self) -> bool:
        """
        Whether the process has beed terminated.
        """
        raise NotImplementedError()

    def isKilled(self) -> bool:
        """
        Whether the process has been killed.
        """
        raise NotImplementedError()

    def timeScheduled(self) -> float:
        """
        Time the process is scheduled and not started (calling run) in seconds.
        """
        raise NotImplementedError()

    def timeRunning(self) -> float:
        """
        Time the process is running (call of run) in seconds.
        """
        raise NotImplementedError()

    def timeout(self) -> float:
        """
        Calculated timeout of the process.
        :raise: NotYetStartedError: if the process is not yet started.
        """
        raise NotImplementedError()

    def estimatedTimeout(self) -> float:
        """
        Estimated timeout of the process. If the timeouts has allready been calculatd the result is equal to ```timeout()```.
        Otherwise timeout is precalulated and may be differ from the finally used timeout.
        """
        raise NotImplementedError()

    def cancel(self):
        """
        Cancle the process.
        Does nothing if the process is already started or terminated.
        :return: whether the process has been cancled
        """
        raise NotImplementedError()

    def terminate(self):
        """
        Terminate the process. An implementation should signal the process to stop, allows a graceful stop.
        Prevent execution if the process is not yet started.
        Does nothing if the process is already finished.
        """
        raise NotImplementedError()

    def kill(self):
        """
        Kill the process. An implementation should stop the process as fast as possible.
        Prevent execution if the process is not yet started.
        Does nothing if the process is already finished.
        """
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
