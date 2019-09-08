from tptp.core.szs import SZSStatus
from tptp.reasoning import SolverResult


class LocalSolverResult(SolverResult):
    def __init__(self, call, szs: SZSStatus, cpu: float, wc: float, stdout:str, stderr:str, returnCode:int):
        super().__init__(call, szs, cpu, wc)
        self._stdout = stdout
        self._stderr = stderr
        self._returnCode = returnCode

    def stdout(self):
        return self._stdout

    def stderr(self):
        return self._stderr

    def returnCode(self):
        return self._returnCode

