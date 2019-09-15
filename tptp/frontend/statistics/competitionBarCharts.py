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

        solverNames = []
        sumCorrect = []
        textList = []
        for s in solvers:
            solverNames.append(str(s))
            sumCorrect.append(len(list(filter(lambda r: r.matches().isCorrect(), dictResults[s]))))
            #sumUnsound = sumCorrect.append(len(list(filter(lambda r: r.matches().isUnsound(), dictResults[s]))))
            timeCorrect = sum(map(lambda r: r.wc if r.matches().isCorrect() else 0, dictResults[s]))

            textList.append('{m:02d}:{s:02d}.{ms:04d}{t}'.format(
                m=int(timeCorrect/60),
                s=int(timeCorrect)%60,
                ms=int(timeCorrect*1000)%1000,
                t=(' - ' + text[s]) if (s in text) else ''
            ))

        NAMES_TITLE = 'number of correct solutions'
        SOLVERS_TITLE = None

        textPositions = list(map(lambda s: 'inside' if s > 0 else 'outside', sumCorrect))

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
            xValues = sumCorrect
            yValues = solverNames
            xTitle = NAMES_TITLE
            yTitle = SOLVERS_TITLE
        else:
            xValues = solverNames,
            yValues = sumCorrect
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

