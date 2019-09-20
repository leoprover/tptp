import pytest

from tptp.reasoning.systemOnTPTP import getSolvers, SystemOnTPTPSolverCall
from .. import common


@pytest.fixture(scope="session")
def fixture_getSolvers():
    return getSolvers()

def test_listing_of_solvers(fixture_getSolvers):
    assert len(fixture_getSolvers) != 0
    for s in fixture_getSolvers:
        assert s.name != None
        assert s.name != ''
        assert s.command != None
        assert s.command != ''


def test_solvers(fixture_getSolvers):
    testSolvers = []
    for s in fixture_getSolvers:
        if 'Leo' in s.name:
            testSolvers.append(s)
    problems = common.getTestProblems(type='THF', status='Theorem')
    for p in problems:
        for s in testSolvers:
            call = SystemOnTPTPSolverCall(p, solver=s, timeout=60)
            result = call.run()
            #print('assert', p.name, s.name, 'expects', p.szsStatus, 'gets', result.szsStatus)
            assert result.szsStatus == p.szsStatus
