from concurrent import futures 

class ReasoningExecuter:
    def __init__(self):
        self._executer = futures.ThreadPoolExecutor(max_workers=threads)

    def schedule(call:SolverCall):
        '''
        Submit a new task, for execution. 
        '''
        logger.debug('schedule {}'.format(task))
        self._scheduledTasks.append(task)
        self._refillActiveTasks()
