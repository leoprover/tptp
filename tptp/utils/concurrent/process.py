class NotYetStartedError(Exception):
    pass

class Process:
    def isStarted(self) -> bool:
        """
        Whether to process has already been started.
        """

    def isRunning(self) -> bool:
        """
        Whether the process is currently running.
        """

    def isDone(self) -> bool:
        """
        Whether the process is done with execution.
        """

    def isTimeout(self) -> bool:
        """
        Whether the process was killed by an external timeout.
        """

    def isInterupted(self) -> bool:
        """
        Whether the process has beed tried to be canceled, terminated or killed.
        """

    def isCanceled(self) -> bool:
        """
        Whether the process has beed canceled.
        """

    def isTerminated(self) -> bool:
        """
        Whether the process has beed terminated.
        """

    def isKilled(self) -> bool:
        """
        Whether the process has been killed.
        """

    def timeout(self) -> float:
        """
        Calculated timeout of the process.
        :raise: NotYetStartedError: if the process is not yet started
        """
        raise NotImplementedError()

    def cancle(self):
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

    def wc(self) -> int:
        """
        Get time running in ms
        """

    def run(self):
        raise NotImplementedError()
