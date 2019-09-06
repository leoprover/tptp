from concurrent.futures import ThreadPoolExecutor, TimeoutError, CancelledError
from typing import Dict

import requests
from typing import Callable

class AsyncPostRequest:
    def __init__(self, url:str, payload:Dict, timeout,
                 callbackSuccess:Callable=None,
                 callbackCancelled:Callable=None,
                 callbackTimeout:Callable=None):
        self.url = url
        self.payload = payload
        self.started = False
        self.timeout = timeout
        self.hasBeenCancelled = False
        self.callbackSuccess = callbackSuccess
        self.callbackCancelled = callbackCancelled
        self.callbackTimeout = callbackTimeout

    def start(self):
        if hasattr(self.timeout, '__call__'):
            self.calculatedTimeout = self.timeout()
        elif isinstance(self.timeout, int):
            self.calculatedTimeout = self.timeout
        else:
            raise Exception("Timeout has to be either an integer or a callable object.")
        self.started = True
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.executor = executor
            self.resultFuture = executor.submit(requests.post,self.url, data=self.payload, timeout=self.calculatedTimeout)
            self.resultFuture.add_done_callback(self._callbackChooser)

    def _callbackChooser(self, future):
        '''
        Selects the appropriate callback when the future is finished
        :return:
        '''
        assert(self.finished())
        try:
            self.resultFuture.result()
        except TimeoutError:
            if self.callbackTimeout:
                self.callbackTimeout()
        except CancelledError:
            if self.callbackCancelled:
                self.callbackCancelled()
        if self.callbackSuccess:
            self.callbackSuccess(self.result())

    def finished(self) -> bool:
        '''
        True iff the request has received a response or the request has been cancelled.
        :return:
        '''
        if not self.started:
            return False
        if self.resultFuture.done():
            return True
        return False

    def cancelled(self):
        '''
        True iff the request has been cancelled using method cancel.
        :return:
        '''
        return self.hasBeenCancelled

    def cancel(self) -> None:
        '''
        Cancels the request i.e. the thread is terminated.
        :return:
        '''
        if not self.started:
            raise Exception("Request not started.")
        self.resultFuture.cancel()
        self.hasBeenCancelled = True

    def wait(self) -> None:
        '''
        Waits until the request is finished or cancelled.
        :return:
        '''
        self.executor.shutdown(wait=True)

    def result(self) -> requests.Response:
        '''
        Returns the response of the request.
        :return:
        '''
        if not self.started:
            raise Exception("Request not started.")
        if not self.resultFuture.done():
            raise Exception("Request not finished.")
        if self.resultFuture.cancelled():
            raise Exception("Request was cancelled.")
        return self.resultFuture.result()

    def calculatedTimeout(self) -> float:
        if not self.started:
            raise Exception("Request not started.")
        return self.calculatedTimeout

    def timeout(self):
        return self.timeout