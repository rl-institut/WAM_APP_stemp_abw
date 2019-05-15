import pandas as pd
from numpy.random import random
from stemp_abw.visualizations import highcharts
from stemp_abw.models import Scenario

from oemof.outputlib import views


class Results(object):
    """Results"""
    def __init__(self, simulation):
        self.results_raw = None
        self.param_results_raw = None
        self.simulation = simulation
        self.is_up_to_date = False
        self.result_id = 0

    def set_result_raw_data(self, results_raw, param_results_raw):
        self.results_raw = results_raw
        self.param_results_raw = param_results_raw
        self.is_up_to_date = True


    def get_node_results_df(self, node_label):
        """Return DataFrame with Checks for existence of node in energy system

        Parameters
        ----------
        node_label : :obj:`str`
            Label of node the data should be looked up for
        """
        if node_label in [str(n) for n in self.simulation.esys.nodes]:
            return views.node(self.results_raw, node_label)
        else:
            raise ValueError(f'Node "{node_label}" not found in energy system!')

    def get_panel_results(self):
        """Analyze results and return data for panel display"""
        #sq_results = self.aggregate_gen_energy(scenario=self.simulation)
        #self.aggregate_gen_energy(scenario=self.simulation.session.user_scenario)

        # temp data
        data = pd.DataFrame({'name': ['Windenergie', 'Photovoltaik', 'Biogas', 'fossil', 'IMPORT'],
                             'y': [2000, 140, 130, 250, 1000]})
        data.set_index('name', inplace=True)

        # convert data to appropriate format for pie chart
        data = {'hc_res_summary_scn': data.reset_index().to_dict(orient='records'),
                'hc_res_wind_time': [1, 2, 3, 4, 5, 4, 3, 2, 1, 8, 0]}
        return data

    def get_layer_results(self):
        """Analyze results and return data for layer display"""
        pass

    def aggregate_gen_energy(self, scenario):
        """Aggregate results for scenario

        TODO: Check if aggregation is fast enough on demand, precalculate if not

        Parameters
        ----------
        scenario
        """
        nodes = []
        return None



class ResultAnalysisVisualization(object):
    """
    Scenarios are loaded, analyzed and visualized within this class

    Implements the Facade Pattern.
    """
    def __init__(self, setup_labels, data_labels, type):
        # datetime_index = [d.strftime('%m') for d in pd.date_range(start='2017-01-01 00:00:00',
        #                                end='2017-12-31 23:00:00',
        #                                freq='1m')]
        index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        timesteps = len(index)
        self.data = pd.DataFrame(index=index,
                                 data={dl: (random(timesteps)*10).round(2) for dl in data_labels})
        self.setup_labels = setup_labels
        self.type = type

    def visualize(self, **kwargs):
        if self.type == 'line':
            visualization = highcharts.HCTimeseries(
                data=self.data,
                setup_labels=self.setup_labels,
                style='display: inline-block',
                **kwargs
            )
        elif self.type == 'pie':
            # temp data
            data = pd.DataFrame({'name': ['Windenergie', 'Photovoltaik', 'Biogas', 'fossil', 'IMPORT'],
                                 'y': [1150, 540, 130, 850, 1300]})
            data.set_index('name', inplace=True)

            # convert data to appropriate format for pie chart
            data = data.reset_index().to_dict(orient='records')

            visualization = highcharts.HCPiechart(
                data=data,
                setup_labels=self.setup_labels,
                style='display: inline-block',
                **kwargs
            )
        elif self.type == 'column':
            visualization = highcharts.HCStackedColumn(
                data=self.data,
                setup_labels=self.setup_labels,
                style='display: inline-block',
                **kwargs
            )
        else:
            raise ValueError
        return visualization
