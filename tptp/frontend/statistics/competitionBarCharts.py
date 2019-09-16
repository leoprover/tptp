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
        numSolvers = len(solvers)
        
        solverNames = []
        numCorrect = []
        numIncorrect = []
        textListCorrect = []
        textListIncorrect = []
        for s in solvers:
            _num = len(dictResults[s])
            _numCorrect = len(list(filter(lambda r: r.matches().isCorrect(), dictResults[s])))
            _isUnsound = len(list(filter(lambda r: r.matches().isUnsound(), dictResults[s]))) > 0
            _timeCorrect = sum(map(lambda r: r.wc if r.matches().isCorrect() else 0, dictResults[s]))

            solverNames.append(str(s))
            numCorrect.append(_numCorrect)
            numIncorrect.append(_num - _numCorrect)

            textListCorrect.append('{m:02d}:{s:02d}.{ms:04d}'.format(
                m=int(_timeCorrect/60),
                s=int(_timeCorrect)%60,
                ms=int(_timeCorrect*1000)%1000,
            ))
            textListIncorrect.append('{state}'.format(
                state='unsound' if _isUnsound else ''
            ))

        NAMES_TITLE = 'number of correct solutions'
        SOLVERS_TITLE = None

        if coloring:
            colorList = list(map(lambda s: coloring[s], solvers))
        else:
            if numSolvers <= len(DECENT_COLORS):
                colorList = DECENT_COLORS
            elif numSolvers <= len(NAMED_CSS_COLORS):
                colorList = NAMED_CSS_COLORS
            else:
                colorList = list(range(numSolvers))

        if orientation == 'h':
            xValuesCorrect = numCorrect
            yValuesCorrect = solverNames
            xValuesIncorrect = numIncorrect
            yValuesIncorrect = solverNames
            xTitle = NAMES_TITLE
            yTitle = SOLVERS_TITLE
        else:
            xValuesCorrect = solverNames
            yValuesCorrect = numCorrect
            xValuesIncorrect = solverNames
            yValuesIncorrect= numIncorrect
            xTitle = SOLVERS_TITLE
            yTitle = NAMES_TITLE

        fig = go.Figure(data=[
            go.Bar(
                x=xValuesCorrect,
                y=yValuesCorrect,
                marker_color=colorList,
                orientation=orientation,
                text=textListCorrect,
                textposition='inside',
            ),
            go.Bar(
                x=xValuesIncorrect,
                y=yValuesIncorrect,
                marker_color=['lightgray']*numSolvers,
                orientation=orientation,
                text=textListIncorrect,
                textposition='inside',
            ),
        ])
        xAxisDict = {
            'title': xTitle,
        }
        yAxisDict = {
            'title': yTitle,
        }
        fig.update_layout(
            barmode='stack',
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

