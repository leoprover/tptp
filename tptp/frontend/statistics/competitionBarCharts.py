from typing import Iterable, Dict
import plotly.graph_objects as go

from .common import createDict, sortSolvers
from ...utils.color import DECENT_COLORS, NAMED_CSS_COLORS
from ...reasoning import SolverResult, Solver
from .dummyResults import dummyResults



class SolvedChart:
    def __init__(self, name:str, *, results:Iterable[SolverResult]):
        self.name = name
        self.results = results

    def __repr__(self):
        return self.__class__.__name__ + self.name

    def figure(self):
        raise NotImplementedError

    def saveFigure(self, width=None, height=None):
        pass # TODO

class SolvedPerSolverChart(SolvedChart):
    """
    Every solver possesses one bar that accounts for successfully solved problems.
    """
    def __init__(self, name: str, *, results: Iterable[SolverResult]):
        super().__init__(name, results=results)

    def figure(self, *,
        orientation='h', 
        solvedAxisWidth:int=None, 
        coloring:Dict[Solver,str]=None, 
        text:Dict[Solver,str]=None
    ):
        dictResults = createDict(self.results)
        solvers = sortSolvers(dictResults.keys())

        solvers = sortSolvers(dictResults.keys())
        solverNames = list(map(lambda s: s.name + s.version if s.version else s.name, solvers))
        sums = list(map(lambda s: len(list(filter(lambda r: r.matches().isCorrect(), dictResults[s]))), solvers))

        NAMES_TITLE = 'number of correct solutions'
        SOLVERS_TITLE = None



        if text:
            textList = list(map(lambda s: text[s] if s in text else None, solvers))
        else:
            textList = None
        textPositions = list(map(lambda s: 'inside' if s > 0 else 'outside', sums))

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

        fig = go.Figure(data=[
            go.Bar(
                x=xValues,
                y=yValues,
                marker_color=colorList,
                orientation=orientation,
                text=textList,
                textposition=textPositions,
            ),
        ])
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

