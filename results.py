import pandas as pd
from numpy.random import random
from stemp_abw import visualizations
#from stemp_abw import visualizations


class ResultAnalysisVisualization(object):
    """
    Scenarios are loaded, analyzed and visualized within this class

    Implements the Facade Pattern.
    """
    def __init__(self, title, captions, type):
        # datetime_index = [d.strftime('%m') for d in pd.date_range(start='2017-01-01 00:00:00',
        #                                end='2017-12-31 23:00:00',
        #                                freq='1m')]
        index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        timesteps = len(index)
        self.data = pd.DataFrame(index=index,
                                 data={c: (random(timesteps)*10).round(2) for c in captions})
        self.title = title
        self.type = type
        #self.data = random(100)
        #self.data = pd.Series(random(10), name='test')

    def visualize(self):
        if self.type == 'line':
            visualization = visualizations.HCTimeseries(
                data=self.data,
                title=self.title,
                style='display: inline-block'
            )
        elif self.type == 'pie':
            visualization = visualizations.HCPiechart(
                data=self.data,
                title=self.title,
                style='display: inline-block'
            )
        else:
            raise ValueError
        return visualization
