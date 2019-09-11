import plotly.graph_objects as go


class SolvedChart:
    def __init__(self, name:str, results):
        self._name = name
        self._results = results

    def __repr__(self):
        return self.__class__.__name__ + self._name

    def figure(self):
        raise NotImplementedError

    def saveFigure(self, width=None, height=None):
        pass # TODO


class SolvedPerSolverChart(SolvedChart):
    """
    Every solver possesses one bar that accounts for successfully solved problems.
    """
    def figure(self, orientation='h'):

        fig = go.Figure(go.Bar(
                    x=[20, 14, 23],
                    y=['giraffes', 'orangutans', 'monkeys'],
                    orientation=orientation))
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

