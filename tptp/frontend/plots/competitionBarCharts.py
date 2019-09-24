from typing import Iterable, Dict, Sequence
import plotly.graph_objects as go

from .common import createDict, sortSolvers
from ...utils.color import DECENT_COLORS, NAMED_CSS_COLORS
from ...reasoning import SolverResult, Solver
from .dummyResults import dummyResults


class SolvedChart:
    def __init__(self, name:str, results:Iterable[SolverResult]):
        self.name = name
        self.results = results

    def __repr__(self):
        return self.__class__.__name__ + self.name

    def traceSolved(self):
        raise NotImplementedError()

    def traceAll(self):
        raise NotImplementedError()

    def traceUnique(self):
        raise NotImplementedError()

    def figure(self):
        raise NotImplementedError()

    def saveFigure(self, width=None, height=None):
        pass # TODO


class SolvedPerSolverChart(SolvedChart):
    """
    Every solver possesses one bar that accounts for successfully solved problems.
    """
    def __init__(self, name: str, results: Iterable[SolverResult]):
        super().__init__(name, results=results)

    def _trace(self,
            computation:str,
            orientation:str='h',
            coloring:Dict[Solver,str]=None,
            text:Dict[Solver,str]=None,
            solverOrder:Sequence=None,
            solverNames:Dict[Solver,str]=None,
        ):
        LEGAL_COMPUTATIONS = ['solved', 'all']
        if not computation in LEGAL_COMPUTATIONS:
            raise Exception('Illegal orientation parameter. Choices are:', str(LEGAL_COMPUTATIONS))
        LEGAL_ORIENTATIONS = ['h', 'v']
        if not orientation in LEGAL_ORIENTATIONS:
            raise Exception('Illegal orientation parameter. Choices are:', str(LEGAL_ORIENTATIONS))

        dictResults = createDict(self.results) # TODO wrap this in a benchmark wrapper

        # establish the order in which solvers are displayed
        if solverOrder:
            solvers = solverOrder
        else:
            solvers = sortSolvers(dictResults.keys())

        # establish names for the solvers
        if solverNames:
            solverNames = list(map(lambda s: solverNames[s], solvers))
        else:
            solverNames = list(map(lambda s: s.name + s.version if s.version else s.name, solvers))

        # calculate result values
        if computation == 'solved':
            values = list(map(lambda s: len(list(filter(lambda r: r.matches().isCorrect(), dictResults[s]))), solvers))
        else: # computation == 'all'
            values = list(map(lambda s: len(dictResults[s]), solvers))

        # establish text displayed on solver bars
        if text:
            textList = list(map(lambda s: text[s] if s in text else None, solvers))
        else:
            textList = None
        textPositions = list(map(lambda s: 'inside' if s > 0 else 'outside', values))

        # establish coloring of solver bars
        if coloring:
            colorList = list(map(lambda s: coloring[s], solvers))
        else:
            if computation == 'solved':
                if len(solvers) <= len(DECENT_COLORS):
                    colorList = DECENT_COLORS
                elif len(solvers) <= len(NAMED_CSS_COLORS):
                    colorList = NAMED_CSS_COLORS
                else:
                    colorList = list(range(len(solvers)))
            else: # computation == 'all'
                colorList = ['lightgrey'] * len(solvers)

        # determine plot values wrt. orientation
        if orientation == 'h':
            xValues = values
            yValues = solverNames
        else:
            xValues = solverNames,
            yValues = values

        # create trace
        trace = go.Bar(
            x=xValues,
            y=yValues,
            marker_color=colorList,
            orientation=orientation,
            text=textList,
            textposition=textPositions,
        )
        return trace

    def traceSolved(self,
            orientation:str='h',
            coloring:Dict[Solver,str]=None,
            text:Dict[Solver,str]=None,
            solverOrder:Sequence=None,
            solverNames:Dict[Solver,str]=None,
        ):
        return self._trace(
            'solved',
            orientation=orientation,
            coloring=coloring,
            text=text,
            solverOrder=solverOrder,
            solverNames=solverNames,
        )

    def traceAll(self,
            orientation:str='h',
            coloring:Dict[Solver,str]=None,
            text:Dict[Solver,str]=None,
            solverOrder:Sequence=None,
            solverNames:Dict[Solver,str]=None
        ):
        return self._trace(
            'all',
            orientation=orientation,
            coloring=coloring,
            text=text,
            solverOrder=solverOrder,
            solverNames=solverNames,
        )

    def traceUnique(self,
            orientation:str='h',
            coloring:Dict[Solver,str]=None,
            text:Dict[Solver,str]=None,
            solverOrder:Sequence=None,
            solverNames:Dict[Solver,str]=None
        ):
        raise NotImplementedError() # TODO

    def figure(self,
           orientation:str='h',
           solvedAxisWidth:int=None,
           coloring:Dict[Solver,str]=None,
           text:Dict[Solver,str]=None,
           solverAxisTitle:str=None,
           solvedAxisTitle:str=None
        ):
        fig =  go.Figure(data=[
            self.traceAll(orientation=orientation),
            self.traceSolved(orientation=orientation, coloring=coloring, text=text),
        ])

        # establish axes titles
        if orientation == 'h':
            xTitle = solvedAxisTitle
            yTitle = solverAxisTitle
        else:
            xTitle = solverAxisTitle
            yTitle = solvedAxisTitle

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
            barmode='overlay', # moves one bar on top of each other
        )

        # establish axes range
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
#fig = chart.figure(solvedAxisWidth=20)
#fig.show()
