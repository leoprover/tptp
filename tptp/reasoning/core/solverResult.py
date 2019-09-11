from tptp.core.szs import SZSStatus


class SolverResult:
    def __init__(self, call, szs:SZSStatus, cpu:float, wc:float):
        self._call = call
        self._szs = szs
        self._cpu = cpu
        self._wc = wc

    def __repr__(self):
        return ','.join(map(lambda x: str(x), [self._szs,self._cpu,self._wc,self._call]))

    def __str__(self):
        return '{szsStatus} for {call}'.format(
            call=self._call,
            szsStatus=self._szs,
        )

    def output(self):
        """
        The raw tptp-conform output of the solver
        """
        raise NotImplementedError()
