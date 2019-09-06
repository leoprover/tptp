from .solverResult import SolverResult
class SolverCall:
    def start(self) -> None:
        '''
        Starts the reasoning call.
        :return:
        '''
        raise NotImplementedError
    def isStarted(self) -> bool:
        '''
        Indicates whether the reasoning call has already started.
        A suspended call is considered started.
        :return:
        '''
        raise NotImplementedError
    def isFinished(self) -> bool:
        '''
        Checks whether the reasoning call is finished and the reasoning result is available.
        :return:
        '''
        raise NotImplementedError
    def suspend(self) -> None:
        '''
        Suspends the reasoning call if applicable and the call has already started.
        If the call has not been started this method does not have any effect.
        :return:
        '''
        raise NotImplementedError
    def isSuspended(self) -> bool:
        '''
        Indicates whether the reasoning call has been suspended.
        If the call has not been started True is returned.
        :return:
        '''
        raise NotImplementedError
    def resume(self) -> None:
        '''
        Resumes a suspended Call
        If the call has not been suspended or the call has not been started this method does not have any effect.
        :return:
        '''
        raise NotImplementedError
    def result(self) -> SolverResult:
        '''
        Returns the result of a started reasoning call.
        This is a blocking method.
        If the reasoning call has not been started this method will throw an exception.
        :return:
        '''
        raise NotImplementedError
    def terminate(self) -> None:
        '''
        Cancels the reasoning call asking the recipient (CLI tool, etc.) of the reasoning call to terminate.
        If the reasoning call has not been started this method will throw an exception.
        If the reasoning call is already finished this method doesnot have any effect.
        :return:
        '''
        raise NotImplementedError
    def kill(self) -> None:
        '''
        Cancels the reasoning call without asking the the recipient (CLI tool, etc.) of the reasoning call to terminate.
        If the reasoning call has not been started this method will throw an exception.
        If the reasoning call is already finished this method doesnot have any effect.
        :return:
        '''
        raise NotImplementedError
    def calculatedTimeout(self) -> float:
        '''
        Returns calculated the timeout.
        If the reasoning call has not been started this method will throw an exception.
        Since a timeout can be a float or a callable object the timeout is evaluated when the method start is invoked.
        :return:
        '''
        raise NotImplementedError
    def timeout(self):
        '''
        Returns the timeout if it is a float or the callable object that calculates the timeout during the start method.
        :return:
        '''
        raise NotImplementedError


