class ProcessExecuter(ThreadedTaskExecuter):
    '''
    Usage:
    * instance.submit(process, timeout) to queue a process for executing
    * instance.wait() to wait for the termination of all submitted processes
    * instance.terminateProcess(process) to manually terminate a process
    * onProcessCompleted(self, process, stdout, stderr) needs to be overwritten
      - is call iff the process finisched. 
      - gets "stdout" and "stderr" of the process.
    * onProcessTimeout(self, process, stdout, stderr) needs to be overwritten
      - is call iff the process is finished by a timeout. 
      - gets "stdout" and "stderr" of the process.
    * onProcessForcedTerminated(self, process, stdout, stderr) needs to be overwritten
      - is call iff the process is terminated by a call of instance.terminate(process) 
      - gets "stdout" and "stderr" of the process.
    * onProcessStart(process) needs to be overloaded
      - is called directly before the process is actual started in a thread
    * onProcessError(self, error) needs to be overloaded
      - is called iff the process is terminated with an exception (file buffer error, or what so ever)
    '''

    def __init__(self, **kwargs):
        super(ThreadProcessExecuter, self).__init__(**kwargs)

    def submit(self, process:Process):
        return super().submit(process)

    def terminate(self, process):
        process.terminate()
