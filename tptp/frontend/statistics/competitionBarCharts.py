from typing import Iterable

import plotly.graph_objects as go

from ...reasoning import SolverResult, Solver
from .dummyResults import dummyResults

def createDict(results:Iterable[SolverResult]):
    d = {}
    for r in results:
        if not r.call.solver in d:
            d[r.call.solver] = []
        d[r.call.solver].append(r)
    return d

class SolvedChart:
    def __init__(self, name:str, results:Iterable[SolverResult]):
        self.name = name
        self.results = results

    def __repr__(self):
        return self.__class__.__name__ + self.name

    def figure(self):
        raise NotImplementedError

    def saveFigure(self, width=None, height=None):
        pass # TODO


def sortSolvers(solvers:Iterable[Solver]):
    return sorted(solvers, key=(lambda s: s.name + str(s.version)))

def sortedSolverNames(solvers:Iterable[Solver]):
    return list(map(lambda s: s.name + s.version if s.version else s.name, sortSolvers(solvers)))

COLORS = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

class SolvedPerSolverChart(SolvedChart):
    """
    Every solver possesses one bar that accounts for successfully solved problems.
    """
    def __init__(self, name: str, results: Iterable[SolverResult]):
        super().__init__(name, results)

    def figure(self, orientation='h'):
        dictResults = createDict(self.results)
        print(dictResults)
        solvers = sortSolvers(dictResults.keys())
        solverNames = list(map(lambda s: s.name + s.version if s.version else s.name, solvers))
        sums = list(map(lambda s: len(dictResults[s]), solvers))

        print("NAMES",solverNames)
        print("SUMS",sums)
        NAMES_TITLE = 'number of solutions'
        SOLVERS_TITLE = None
        if orientation == 'h':
            print("orient")
            xValues = sums
            yValues = solverNames
            xTitle = NAMES_TITLE
            yTitle = SOLVERS_TITLE
        else:
            xValues = solverNames,
            yValues = sums
            xTitle = SOLVERS_TITLE
            yTitle = NAMES_TITLE
        fig = go.Figure(go.Bar(
            x=xValues,
            y=yValues,
            marker_color=COLORS,
            orientation=orientation
        ))
        fig.update_layout(
            title=self.name,
            showlegend=False,
            legend_orientation="h",
            xaxis=dict(
                title=xTitle
            ),
            yaxis=dict(
                title=yTitle,
            ),
        )

        fig.show()
        return fig



class SolvedPerConfigurationPerSolver(SolvedChart):
    """
    Every Configuration possesses its own plot.
    Each such plot possesses one bar for every solver that accounts for successfully solved problems.
    """
    pass

class SolvedPerSolverPerConfigurationIntegrated(SolvedChart):
    """
    Every solver possesses one bar that accounts for successfully solved problems.
    Each such bar is partitioned such that every configuration gets a slice of the bar representing the number of successfully solved problems.
    """
    pass

chart = SolvedPerSolverChart('myplot', dummyResults)
chart.figure()

