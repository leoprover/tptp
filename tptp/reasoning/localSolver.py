from tptp.core.szs import SZSStatus
from tptp.reasoning import SolverResult


class LocalSolverResult(SolverResult):
    def __init__(self, call, szs: SZSStatus, cpu: float, wc: float, configuration=None):
        super().__init__(call, szs, cpu, wc, configuration)

