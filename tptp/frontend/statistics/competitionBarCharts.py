from typing import Iterable, Dict
import plotly.graph_objects as go

from ...utils.color import DECENT_COLORS, NAMED_CSS_COLORS
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

class SolvedPerSolverChart(SolvedChart):
    """
    Every solver possesses one bar that accounts for successfully solved problems.
    """
    def __init__(self, name: str, results: Iterable[SolverResult]):
        super().__init__(name, results)

    def figure(self, orientation='h', solvedAxisWidth:int=None, coloring:Dict[Solver,str]=None):
        dictResults = createDict(self.results)
        solvers = sortSolvers(dictResults.keys())
        solverNames = list(map(lambda s: s.name + s.version if s.version else s.name, solvers))
        sums = list(map(lambda s: len(list(filter(lambda r: r.matches().isCorrect(), dictResults[s]))), solvers))

        NAMES_TITLE = 'number of solutions'
        SOLVERS_TITLE = None

        if coloring:
            colorList = list(map(lambda s: coloring[s], solvers))
        else:
            if len(solvers) <= len(DECENT_COLORS):
                colorList = DECENT_COLORS
            elif len(solvers) <= len(NAMED_CSS_COLORS):
                colorList = NAMED_CSS_COLORS
            else:
                colorList = list(range(len(solvers)))

        if orientation == 'h':
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
            marker_color=colorList,
            orientation=orientation,
        ))
        xAxisDict = {
            'title': xTitle,
        }
        yAxisDict = {
            'title': yTitle,
        }
        fig.update_layout(
            title=self.name,
            showlegend=False,
            xaxis=xAxisDict,
            yaxis=yAxisDict,
        )
        if orientation == 'h':
            if solvedAxisWidth:
                fig.update_xaxes(range=[0, solvedAxisWidth])
        else:
            if solvedAxisWidth:
                fig.update_yaxes(range=[0, solvedAxisWidth])
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

#chart = SolvedPerSolverChart('myplot', dummyResults)
#chart.figure(solvedAxisWidth=20)

