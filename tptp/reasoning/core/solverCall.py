from .solverResult import SolverResult

class SolverCall:
    def __str__(self):
        return '{problem} with {solver} -t {timeout}s'.format(
            solver=self._solver,
            problem=self._problem,
            timeout=self.estimatedTimeout(),
        )

    @property
    def solver(self):
        return self._solver

    @property
    def problem(self):
        return self._problem

    def run(self) -> SolverResult:
        """
        Runs the reasoning call.
        This is a blocking method.
        May be called in a different thread.

        Use concurrent.futures.Executor.submit to run this in a different thread
        :return:
        """
        raise NotImplementedError()

    def isStarted(self) -> bool:
        """
        Indicates whether the reasoning call has already started.
        A suspended call is considered started.
        :return:
        """
        raise NotImplementedError()
    
    def isRunning(self) -> bool:
        """
        Indicates whether the reasoning call is currently running.
        :return:
        """
        raise NotImplementedError()

    def isDone(self) -> bool:
        """
        Checks whether the reasoning call is finished and the reasoning result is available.
        :return:
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

    def cancel(self) -> None:
        """
        If the reasoning call has not been started the start will be prevented.
        If the reasoning call is already finished this method doesnot have any effect.
        :return:
        """
        raise NotImplementedError()
    
    def terminate(self) -> None:
        """
        Terminates the reasoning call asking the recipient (CLI tool, etc.) of the reasoning call to terminate.
        If the reasoning call has not been started the start will be prevented.
        If the reasoning call is already finished this method doesnot have any effect.
        :return:
        """
        raise NotImplementedError()
    
    def kill(self) -> None:
        """
        Cancels the reasoning call without asking the the recipient (CLI tool, etc.) of the reasoning call to kill.
        If the reasoning call has not been started the start will be prevented.
        If the reasoning call is already finished this method doesnot have any effect.
        :return:
        """
        raise NotImplementedError()
    
    def timeout(self) -> float:
        """
        Estimated timeout of the call. If the timeouts has allready been calculatd the result is equal to ```timeout()```.
        Otherwise timeout is precalulated and may be differ from the finally used timeout.
        :return:
        """
        raise NotImplementedError()
    
    def estimatedTimeout(self) -> float:
        """
        Returns calculated the timeout if one is available, otherwise it precalculates the timeout a gives an estimation.
        :return:
        """
        raise NotImplementedError()

    def estimatedRuntimeLeft(self) -> float:
        """
        Estimated runtime left of the solver call if it is reaching its timeout.
        :return:
        """
        if self.isDone():
            return 0
        return self.estimatedTimeout() - self.timeRunning()

    # the following is optional
    #def suspend(self) -> None:
    #    """
    #    Suspends the reasoning call if applicable and the call has already started.
    #    If the call has not been started this method does not have any effect.
    #    :return:
    #    """
    #    raise NotImplementedError
    #def isSuspended(self) -> bool:
    #    """
    #    Indicates whether the reasoning call has been suspended.
    #    If the call has not been started True is returned.
    #    :return:
    #    """
    #    raise NotImplementedError
    #def resume(self) -> None:
    #    """
    #    Resumes a suspended Call
    #    If the call has not been suspended or the call has not been started this method does not have any effect.
    #    :return:
    #    """
    #    raise NotImplementedError
