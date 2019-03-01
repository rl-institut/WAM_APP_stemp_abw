import pandas as pd
from numpy.random import random
from stemp_abw import visualizations
#from stemp_abw import visualizations


class ResultAnalysisVisualization(object):
    """
    Scenarios are loaded, analyzed and visualized within this class

    Implements the Facade Pattern.
    """
    def __init__(self, title, captions):
        # datetime_index = [d.strftime('%m') for d in pd.date_range(start='2017-01-01 00:00:00',
        #                                end='2017-12-31 23:00:00',
        #                                freq='1m')]
        index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        timesteps = len(index)
        self.data = pd.DataFrame(index=index,
                                 data={c: (random(timesteps)*10).round(2) for c in captions})
        self.title = title
        #self.data = random(100)
        #self.data = pd.Series(random(10), name='test')

    def visualize(self):
        visualization = visualizations.HCTimeseries(
            data=self.data,
            title=self.title
            # Note: inline-block originally used to make sure the graph is
            # scaled correctly even if the expansion of the result panel has
            # not finished before the HC graphs are loaded. Deactivated since
            # the graphs do not scale properly if window is resized.
            #style='display: inline-block'
        )
        return visualization
