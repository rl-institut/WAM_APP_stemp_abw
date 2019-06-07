import pandas as pd
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
        """Return DataFrame with optimization results (timeseries) for single
        node.

        Parameters
        ----------
        node_label : :obj:`str`
            Label of node the data should be looked up for

        Returns
        -------
        :pandas:`pandas.DataFrame<dataframe>`
            Node results (timeseries)
        """
        if node_label in [str(n) for n in self.simulation.esys.nodes]:
            return views.node(self.results_raw, node_label)
        else:
            raise ValueError(f'Node "{node_label}" not found in energy system!')

    def get_result_charts_data(self):
        """Analyze results and return data for panel display"""

        #####################
        # Energy production #
        #####################
        # node sources and targets
        nodes_from = ['gen_el_wind',
                      'gen_el_pv_ground',
                      'gen_el_pv_roof',
                      'gen_el_hydro',
                      'shortage_el']
        nodes_to = ['bus_el']

        # aggregate raw data
        data_power_prod_user_scn = self.agg_energy_sum_per_flow(nodes_from,
                                                                nodes_to,
                                                                self.results_raw)
        data_power_prod_sq_scn = self.agg_energy_sum_per_flow(nodes_from,
                                                              nodes_to,
                                                              self.sq_results_raw)

        # prepare chart data
        hc_column_power_prod_both_scn = [{'name': k1, 'data': [v1, v2]}
                                         for (k1, v1), (k2, v2) in
                                         zip(data_power_prod_user_scn,
                                             data_power_prod_sq_scn)]


        hc_pie_power_production_user_scn = [{'name': k, 'y': v}
                                            for (k, v) in data_power_prod_user_scn]
        hc_pie_power_production_sq_scn = [{'name': k, 'y': v}
                                          for (k, v) in data_power_prod_sq_scn]

        #################
        # Energy demand #
        #################
        # node sources and targets
        nodes_from = ['bus_el']
        nodes_to = ['dem_el_hh',
                    'dem_el_rca',
                    'dem_el_ind',
                    'excess_el']

        # aggregate raw data
        data_power_dem_user_scn = self.agg_energy_sum_per_flow(nodes_from,
                                                               nodes_to,
                                                               self.results_raw)
        data_power_dem_sq_scn = self.agg_energy_sum_per_flow(nodes_from,
                                                             nodes_to,
                                                             self.sq_results_raw)

        # prepare chart data
        hc_column_power_dem_both_scn = [{'name': k1, 'data': [v1, v2]}
                                        for (k1, v1), (k2, v2) in
                                        zip(data_power_dem_user_scn,
                                            data_power_dem_sq_scn)]

        ###################
        # Own consumption #
        ###################
        data_power_prod_user_scn_sum = sum([v for (k,v)
                                            in data_power_prod_user_scn
                                            if k != 'Import'])
        data_power_prod_sq_scn_sum = sum([v for (k, v)
                                          in data_power_prod_sq_scn
                                          if k != 'Import'])
        data_power_dem_user_scn_sum = sum([v for (k,v)
                                           in data_power_dem_user_scn
                                           if k != 'Export'])
        data_power_dem_sq_scn_sum = sum([v for (k, v)
                                         in data_power_dem_sq_scn
                                         if k != 'Export'])

        # prepare chart data
        hc_column_power_own_cons_both_scn = [
            {'name': 'Eigenversorgung',
             'data': [round(data_power_prod_user_scn_sum /
                            data_power_dem_user_scn_sum * 100, 1),
                      round(data_power_prod_sq_scn_sum /
                            data_power_dem_sq_scn_sum * 100, 1)]}
        ]

        ######################
        # make dict for json #
        ######################
        chart_data = {
            'hc_column_power_prod_both_scn': hc_column_power_prod_both_scn,
            'hc_column_power_dem_both_scn': hc_column_power_dem_both_scn,
            'hc_column_power_own_cons_both_scn' : hc_column_power_own_cons_both_scn,
            'hc_pie_power_production_user_scn': hc_pie_power_production_user_scn,
            'hc_pie_power_production_sq_scn': hc_pie_power_production_sq_scn,
            'hc_res_wind_time': [5, 5, 5, 4, 2, 0, 2, 8, 1, 7, 1]
        }

        return chart_data

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
