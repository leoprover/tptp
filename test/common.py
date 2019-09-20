import glob

from pathlib import Path
from typing import List

from tptp.core import ProblemWithStatus, SZSStatus


def getDataDirectory() -> Path:
    return Path(__file__).parent / 'data'

def getTPTPProblemsDirectory(status=None) -> Path:
    dir =  getDataDirectory() / 'tptp_problems'
    if status:
        assert status in ['Theorem', 'CounterSatisfiable']
        dir /= status
    return dir

def getFiles(path:Path, extension=''):
    return [f for f in glob.glob(str(path) + "**/*" + extension, recursive=True)]

def getTypeDict():
    typeDict = {
        'THF': '^',
        'TFF_WOA': '_',
        'TFF': '=',
        'FOF': '+',
        'CNF': '-',
    }
    return typeDict

def getTestProblemPaths(type=None, status=None) -> List[Path]:
    typeDict = getTypeDict()
    if type:
        assert type in typeDict
        problems = (filter(lambda f: typeDict[type] in f.name,
                           map(lambda p: Path(p), getFiles(getTPTPProblemsDirectory(status=status), extension='.p'))))
    else:
        problems = (map(lambda p: Path(p), getFiles('tptp_problems', extension='.p')))
    return list(problems)

def getTestProblems(type=None, status=None) -> List[ProblemWithStatus]:
    problemPaths = getTestProblemPaths(type, status=status)
    return list(map(lambda p: ProblemWithStatus(p.name, p, p.read_text(), SZSStatus.get(status)), problemPaths))
