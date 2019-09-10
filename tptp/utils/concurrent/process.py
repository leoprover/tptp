class NotYetStartedError(Exception):
    pass

class Process:
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
