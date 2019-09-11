import logging
import subprocess
import os
import signal

logger = logging.getLogger(__name__)

from .timer import Timer
from .process import Process, NotYetStartedError


class LocalProcess(Process):
    INITIALIZED = 1
    
    STARTED = 2
    FORCED_TERMINATE_SEND = 3
    FORCED_KILL_SEND = 4

    CANCELLED = 5
    COMPLETED = 6
    TIMEOUT = 7
    FORCED_TERMINATED = 8
    FORCED_KILLED = 9
    
    def __init__(self, call=None, *, timeout=None):
        self._timeout = timeout
        self._call = call

        self._timeout_calculated = None
        self._call_calculated = None

        self.timer = Timer()
        self.timer.schedule()
        self._state = self.INITIALIZED
        self._isForcedTerminated = False
        self._isForcedKilled = False
        self._isTimeout = False
        self._cancled = False

    def isStarted(self) -> bool:
        """
        Whether to process has already been started.
        """
        return self._state >= self.STARTED

    def isRunning(self) -> bool:
        """
        Whether the process is currently running.
        """
        return self._state in [self.STARTED, self.FORCED_TERMINATE_SEND, self.FORCED_KILL_SEND]

    def isDone(self) -> bool:
        """
        Whether the process is done with execution.
        """
        return self._state >= self.CANCELLED

    def isTimeout(self) -> bool:
        """
        Whether the process was killed by an external timeout.
        """
        return self._state == self.TIMEOUT

    def isInterupted(self) -> bool:
        """
        Whether the process has beed tried to be canceled, terminated or killed.
        """
        return self._state in [self.FORCED_TERMINATE_SEND, self.FORCED_KILL_SEND, self.CANCELLED, self.FORCED_TERMINATED, self.FORCED_KILLED]

    def isCanceled(self) -> bool:
        """
        Whether the process has beed canceled.
        """
        return self._state == self.CANCELLED

    def isTerminated(self) -> bool:
        """
        Whether the process has beed terminated.
        """
        return self._state == self.FORCED_TERMINATED

    def isKilled(self) -> bool:
        """
        Whether the process has been killed.
        """
        return self._state == self.FORCED_KILLED

    def timeScheduled(self) -> float:
        """
        Time the process is scheduled and not started (calling run) in seconds.
        """
        return self.timer.getTimeScheduled()

    def timeRunning(self) -> float:
        """
        Time the process is running (call of run) in seconds.
        """
        return self.timer.getTimeRunning()

    def start(self):
        if callable(self._timeout) or hasattr(self._timeout, '__call__'):
            self._timeout_calculated = self._timeout()
        else:
            self._timeout_calculated = self._timeout

        if callable(self._call) or hasattr(self._call, '__call__'):
            self._call_calculated = self._call(self._timeout_calculated)
        else:
            self._call_calculated = self._call

        if self._state == self.CANCELLED:
            return

        self.timer.start()
        # if terminated or killed, skip execution
        if self._isForcedTerminated or self._isForcedKilled:
            self.timer.end()
            if self._isForcedTerminated:
                self._state = self.FORCED_TERMINATED
            if self._isForcedKilled:
                self._state = self.FORCED_KILLED
            return

        self._state = self.STARTED

        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before exec() to run the shell.
        # @see https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        self._process = subprocess.Popen(
            self._call_calculated,
            stdout=subprocess.PIPE, # store the stdout in in the subprocess itself
            stderr=subprocess.PIPE, # store the stderr in in the subprocess itself
            preexec_fn=os.setsid,
            env=os.environ,  # use the environment of the python instance, s.t. we can set enviroment variables for started subprocesses
            shell=True,
        )

    def call(self):
        if not self.isStarted():
            raise NotYetStartedError()

        return self._call_calculated

    def estimatedCall(self):
        if not self.isStarted():
            if callable(self._call) or hasattr(self._call, '__call__'):
                self._call_calculated = self._call(self.estimatedTimeout())
            else:
                self._call_calculated = self._call

        return self._call_calculated

    def timeout(self):
        """
        Calculated timeout of the process.
        :raise: NotYetStartedError: if the process is not yet started.
        """
        if not self.isStarted():
            raise NotYetStartedError()

        return self._timeout_calculated

    def estimatedTimeout(self) -> float:
        """
        Estimated timeout of the process. If the timeouts has allready been calculatd the result is equal to ```timeout()```.
        Otherwise timeout is precalulated and may be differ from the finally used timeout.
        """
        if not self.isStarted():
            if callable(self._timeout) or hasattr(self._timeout, '__call__'):
                return self._timeout()
            return self._timeout
        return self._timeout_calculated

    def cancel(self):
        if self.isStarted():
            return False
        self._state = self.CANCELLED

    def terminate(self):
        self._state = self.FORCED_TERMINATE_SEND
        self._isForcedTerminated = True
        self._terminate()


    def kill(self):
        self._state = self.FORCED_KILL_SEND
        self._isForcedKilled = True
        self._kill()

    def _terminate(self):
        '''
        Terminates the underlaying execution.
        '''
        # @see https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        os.killpg(os.getpgid(self._process.pid), signal.SIGTERM)  # Send the signal to all the process groups

    def _kill(self):
        '''
        Kills the underlaying execution.
        @TODO verify: SIGKILL does not work on windows? use signal.SIGTERM maybe?
        '''
        # @see https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)  # Send the signal to all the process groups

    def communicate(self):
        if not self.isStarted():
            raise NotYetStartedError()
        
        try:
            stdout, stderr, returncode = self.communicate0()
        except:
            raise
        finally:
            self.timer.end()
            # set state if anything is terminated
            if self._isTimeout:
                self._state = self.TIMEOUT
            elif self._isForcedTerminated:
                self._state = self.FORCED_TERMINATED
            elif self._isForcedKilled:
                self._state = self.FORCED_KILLED
            else:
                self._state = self.COMPLETED

        stdout_utf8 = stdout.decode('utf8')
        stderr_utf8 = stderr.decode('utf8')

        return stdout_utf8, stderr_utf8, returncode

    def communicate0(self):
        try:
            stdout, stderr, returncode = self.communicate1()
        except:
            #enforce halt in any case
            self._process.kill()
            raise
        return stdout, stderr, returncode

    def communicate1(self):
        if self._timeout:
            try:
                stdout, stderr = self._process.communicate(timeout=self._timeout)
            except subprocess.TimeoutExpired:
                # remember timeout
                self._isTimeout = True
                self._kill()
                stdout, stderr = self._process.communicate()

                self._state = self.TIMEOUT
                return stdout, stderr, self._process.returncode
        else:
            stdout, stderr = self._process.communicate()
        return stdout, stderr, self._process.returncode

    def run(self):
        self.start()
        return self.communicate()

    def stateStr(self):
        return '{state} {timer}/{timeout}s'.format(
            state=self._state,
            timer=self.timer,
            timeout=self._timeout_calculated,
        )

    def __str__(self):
        return '{call}[{state}]'.format(
            call=self._call_calculated,
            state=self.stateStr(),
        )
