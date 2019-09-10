from concurrent.futures import ThreadPoolExecutor, TimeoutError, CancelledError
from typing import Dict

import requests
from typing import Callable

from .process import Process

class AsyncPostRequest(Process):
    # states
    _PENDING = "PENDING"
    _RUNNING = "RUNNING"
    _CANCELLED = "CANCELLED"
    _FINISHED = "FINISHED"

    def __init__(self, url:str, payload:Dict, timeout):
        self._state = AsyncPostRequest._PENDING
        self._url = url
        self._payload = payload
        self._timeout = timeout
        self._callbackSuccess = []
        self._callbackCancelled = []
        self._callbackTimeout = []

    def addCallbackSuccess(self, callback:Callable):
        self._callbackSuccess.append(callback)

    def addCallbackCancelled(self, callback: Callable):
        self._callbackCancelled.append(callback)

    def addCallbackTimeout(self, callback: Callable):
        self._callbackTimeout.append(callback)

    def start(self):
        """
        Starts the asynchronous post request.
        :return:
        """
        if hasattr(self._timeout, '__call__'):
            self._calculatedTimeout = self._timeout()
        elif isinstance(self._timeout, int):
            self._calculatedTimeout = self._timeout
        else:
            raise Exception("Timeout has to be either an integer or a callable object.")
        self._state = AsyncPostRequest._RUNNING
        with ThreadPoolExecutor(max_workers=1) as executor:
            self._executor = executor
            self._resultFuture = executor.submit(requests.post, self._url, data=self._payload, timeout=self._calculatedTimeout)
            self._resultFuture.add_done_callback(self._callbackChooser)

    def _callbackChooser(self, future):
        """
        Selects the appropriate callback when the future is finished
        :return:
        """
        assert(self.done())
        try:
            self._resultFuture.result()
        except TimeoutError:
            for c in self._callbackTimeout:
                c()
        except CancelledError:
            for c in self._callbackCancelled:
                c()
        if self._callbackSuccess:
            for c in self._callbackSuccess:
                c()

    def running(self) -> bool:
        """
        True iff the method started was invoked.
        :return:
        """
        return self._state == AsyncPostRequest._RUNNING

    def done(self) -> bool:
        """
        True iff the request has received a response or the request has been cancelled.
        :return:
        """
        if not self._state == AsyncPostRequest._RUNNING:
            return False
        if self._resultFuture.done():
            return True
        return False

    def cancelled(self):
        """
        True iff the request has been cancelled using the method cancel.
        :return:
        """
        return self._state == AsyncPostRequest._CANCELLED

    def cancel(self) -> None:
        """
        Cancels the request i.e. the thread is terminated.
        :return:
        """
        if not self._state == AsyncPostRequest._RUNNING:
            raise Exception("Request not started.")
        self._hasBeenCancelled = True
        self._resultFuture.cancel()

    def wait(self) -> None:
        """
        Waits until the request is finished or cancelled.
        :return:
        """
        self._executor.shutdown(wait=True)

    def result(self) -> requests.Response:
        """
        Returns the response of the request.
        :return:
        """
        if not self._state == AsyncPostRequest._RUNNING:
            raise Exception("Request not started.")
        if not self._resultFuture.done():
            raise Exception("Request not finished.")
        if self._resultFuture.cancelled():
            raise Exception("Request was cancelled.")
        return self._resultFuture.result()

    def calculatedTimeout(self) -> float:
        if not self._state == AsyncPostRequest._RUNNING:
            raise Exception("Request not started.")
        return self._calculatedTimeout

    def timeout(self):
        return self._timeout