from tptp.core.szs import SZSStatus


class SolverResult:
    def __init__(self, call, szs:SZSStatus, cpu:float, wc:float, configuration=None):
        self.call = call
        self.szs = szs
        self.cpu = cpu
        self.wc = wc
        self.configuration = configuration

    def __repr__(self):
        return ','.join(map(lambda x: str(x), [self.szs,self.cpu,self.wc,self.call]))