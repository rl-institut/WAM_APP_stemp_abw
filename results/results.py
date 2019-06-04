import pandas as pd
from numpy.random import random
from stemp_abw.visualizations import highcharts
from stemp_abw.models import Scenario
from stemp_abw.results.io import oemof_json_to_results
from stemp_abw.app_settings import NODE_LABELS

from oemof.outputlib import views


class Results(object):
    """Results"""
    def __init__(self, simulation):
        self.sq_results_raw, self.sq_param_results_raw = oemof_json_to_results(Scenario.objects.get(
            name='Status quo').results.data)

        self.results_raw = None
        self.param_results_raw = None
        self.simulation = simulation
        self.is_up_to_date = False

        # set SQ results on startup
        self.set_result_raw_data(self.sq_results_raw,
                                 self.param_results_raw)

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

        nodes_from = ['gen_el_wind',
                      'gen_el_pv_roof',
                      'gen_el_pv_ground',
                      'gen_el_hydro',
                      'shortage_el']
        nodes_to = ['bus_el']
        data_user_scn = self.agg_energy_sum_per_flow(nodes_from, nodes_to, self.results_raw)
        data_sq = self.agg_energy_sum_per_flow(nodes_from, nodes_to, self.sq_results_raw)

        # data_user_scn2 = {'Windenergie': [3,6],
        #                   'PV': [1,2],
        #                   'PV2': [2,1]}
        data_user_scn2 = [{'name': 'Windenergie', 'data': [3,6]},
                          {'name': 'PV', 'data': [1,2]},
                          {'name': 'PV2', 'data': [2,1]}]

        # convert data to appropriate format
        data = {'hc_res_summary_scn': data_user_scn2,
                'hc_res_summary_sq': data_sq,
                'hc_res_production_scn': data_user_scn,
                'hc_res_production_sq': data_sq,
                'hc_res_wind_time': [1, 2, 3, 4, 5, 4, 3, 2, 1, 8, 0]}

        return data

    def get_layer_results(self):
        """Analyze results and return data for layer display"""
        pass

    def aggregate_sum(self, nodes_from, nodes_to, results):
        """Aggregate results for scenario

        TODO: Check if aggregation is fast enough on demand, precalculate if not

        Parameters
        ----------
        scenario
        """
        if not (len(nodes_from) == 1 and len(nodes_to) >= 1) and\
           not (len(nodes_to) == 1 and len(nodes_from) >= 1):
            raise ValueError('One of source and target nodes '
                             'must contain exactly 1 node, the '
                             'other >=1 nodes.')

        agg_data = [{'name': NODE_LABELS[n_from],
                     'y': round(results[(n_from, nodes_to[0])]
                                ['sequences']['flow'].sum()/1000)}
                    for n_from in nodes_from]

        return agg_data


class ResultAnalysisVisualization(object):
    """
    Scenarios are loaded, analyzed and visualized within this class
    """
    def __init__(self, setup_labels, data_labels=[], type=None):
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
