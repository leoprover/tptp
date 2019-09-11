from typing import Iterable

from ..core import SolverCall, SolverResult

class ReasoningScheduler():
    """
    Generic interface for a reasoning scheduler.
    """
    def enque(call:SolverCall):
        """
        Enque a new solver call for execution.
        """
        raise NotImplementedError()

    def onSchedule(call:SolverCall):
        """
        Called when the call has been scheduled and before the execution starts.
        """
        raise NotImplementedError()

    def onFinish(result:SolverResult):
        """
        Called when the execution of the call in ```result.call``` has been finished.
        """
        raise NotImplementedError()

    def enquedCalls() -> Iterable[SolverCall]:
        """
        Iterator over enqueued calls.
        """
        raise NotImplementedError()

    def numParallel():
        """
        Number of parallel executions. This number should not exceed the number of available cpu cores. 
        """
        raise NotImplementedError()

    def numEnqued():
        """
        Number of enqued calles.
        Override of speedup.
        """
        return len(self.enquedCalls())

    def estimatedTimeout() -> float:
        """
        Estimated timeout of all enqued solver call.
        """
        t = 0
        for call in self.enquedCalls():
            t += call.estimatedTimeout()
        return t
