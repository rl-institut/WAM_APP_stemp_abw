from stemp_abw.visualizations import highcharts
from stemp_abw.models import Scenario, RegMun
from stemp_abw.results.io import oemof_json_to_results
from stemp_abw.app_settings import NODE_LABELS, SIMULATION_CFG as SIM_CFG

from oemof.outputlib import views

import pandas as pd
from numpy.random import uniform


class Results(object):
    """Results associated to Simulation

    TODO: Complete docstring
    """
    def __init__(self, simulation):
        self.sq_results_raw, self.sq_param_results_raw = oemof_json_to_results(
            Scenario.objects.get(name='Status quo').results.data)

        self.results_raw = self.sq_results_raw
        self.param_results_raw = self.sq_param_results_raw
        self.status = 'init'
        self.simulation = simulation

    def set_result_raw_data(self, results_raw, param_results_raw):
        self.results_raw = results_raw
        self.param_results_raw = param_results_raw
        self.status = 'up_to_date'

    @staticmethod
    def get_raw_results_df(results_raw):
        """Return DataFrame with optimization results (timeseries) for all
        nodes for given raw results

        Parameters
        ----------
        results_raw : :obj:`dict` of :pandas:`pandas.DataFrame`
            Raw result data from optimization as created by oemof

        Returns
        -------
        :pandas:`pandas.DataFrame`
            Node results (timeseries)
        """
        timerange = pd.date_range(start=SIM_CFG['date_from'],
                                  end=SIM_CFG['date_to'],
                                  freq=SIM_CFG['freq'])
        df = pd.concat([v['sequences'].rename(columns={'flow': k})
                        for k, v in results_raw.items()], axis=1)
        df.index = timerange
        return df

    def get_node_results_df(self, node_label):
        """Return DataFrame with optimization results (timeseries) for single
        node.

        Parameters
        ----------
        node_label : :obj:`str`
            Label of node the data should be looked up for

        Returns
        -------
        :pandas:`pandas.DataFrame`
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

        # 1) Annual data (user scenario + SQ)
        #####################################
        # aggregate raw data
        data_power_prod_user_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            self.results_raw,
            resample_mode='A',
            agg_mode='sum'
        )
        data_power_prod_sq_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            self.sq_results_raw,
            resample_mode='A',
            agg_mode='sum'
        )

        # prepare chart data
        hc_column_power_prod_both_scn = [{'name': k1, 'data': [v1[0], v2[0]]}
                                         for (k1, v1), (k2, v2) in
                                         zip(data_power_prod_user_scn,
                                             data_power_prod_sq_scn)]

        hc_pie_power_production_user_scn = [{'name': k, 'y': v[0]}
                                            for (k, v) in data_power_prod_user_scn]
        hc_pie_power_production_sq_scn = [{'name': k, 'y': v[0]}
                                          for (k, v) in data_power_prod_sq_scn]

        # 2) Monthly data (user scenario)
        #################################
        data_power_prod_m_user_scn = self.aggregate_flow_results(
            nodes_from=['gen_el_wind',
                        'gen_el_pv_ground',
                        'gen_el_pv_roof'],
            nodes_to=nodes_to,
            results_raw=self.results_raw,
            resample_mode='M',
            agg_mode='sum'
        )

        data_power_prod_m_user_scn = {k: v
                                      for (k, v) in data_power_prod_m_user_scn}
        data_power_prod_m_user_scn['Photovoltaik'] = [
            round(x1+x2, 1)
            for x1, x2 in zip(data_power_prod_m_user_scn.pop('PV Freifläche'),
                              data_power_prod_m_user_scn.pop('PV Dach'))]
        hc_column_power_prod_m_user_scn = [{'name': k, 'data': v}
                                           for k, v in data_power_prod_m_user_scn.items()]

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
        data_power_dem_user_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            self.results_raw,
            resample_mode='A',
            agg_mode='sum'
        )
        data_power_dem_sq_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            self.sq_results_raw,
            resample_mode='A',
            agg_mode='sum'
        )

        # prepare chart data
        hc_column_power_dem_both_scn = [{'name': k1, 'data': [v1[0], v2[0]]}
                                        for (k1, v1), (k2, v2) in
                                        zip(data_power_dem_user_scn,
                                            data_power_dem_sq_scn)]

        ###################
        # Own consumption #
        ###################
        data_power_prod_user_scn_sum = sum([v[0] for (k,v)
                                            in data_power_prod_user_scn
                                            if k != 'Import'])
        data_power_prod_sq_scn_sum = sum([v[0] for (k, v)
                                          in data_power_prod_sq_scn
                                          if k != 'Import'])
        data_power_dem_user_scn_sum = sum([v[0] for (k,v)
                                           in data_power_dem_user_scn
                                           if k != 'Export'])
        data_power_dem_sq_scn_sum = sum([v[0] for (k, v)
                                         in data_power_dem_sq_scn
                                         if k != 'Export'])

        # prepare chart data
        hc_column_power_own_cons_both_scn = [
            round(data_power_prod_user_scn_sum /
                  data_power_dem_user_scn_sum * 100, 1),
            round(data_power_prod_sq_scn_sum /
                  data_power_dem_sq_scn_sum * 100, 1)]


        ######################
        # make dict for json #
        ######################
        chart_data = {
            'hc_column_power_prod_both_scn': hc_column_power_prod_both_scn,
            'hc_column_power_dem_both_scn': hc_column_power_dem_both_scn,
            'hc_column_power_own_cons_both_scn' : hc_column_power_own_cons_both_scn,
            'hc_pie_power_production_user_scn': hc_pie_power_production_user_scn,
            'hc_pie_power_production_sq_scn': hc_pie_power_production_sq_scn,
            'hc_column_power_prod_m_user_scn': hc_column_power_prod_m_user_scn,
            'hc_res_wind_time': [5, 5, 5, 4, 2, 0, 2, 8, 1, 7, 1]
        }

        return chart_data

    def get_layer_results(self):
        """Analyze results and return data for layer display"""

        results = pd.DataFrame(list(
            RegMun.objects \
                .values_list('ags', named=True)))

        columns = ['energy_re_el_dem_share_result',
                   'gen_energy_re_result',
                   'gen_energy_re_density_result',
                   'gen_cap_re_result',
                   'gen_cap_re_density_result',
                   'gen_count_wind_density_result',
                   'dem_el_energy_result',
                   'dem_el_energy_per_capita_result']

        for c in columns:
            results[c] = [round(_,1) for _ in uniform(low=0, high=100, size=20)]

        results.set_index('ags', inplace=True)

        return results

    def aggregate_flow_results(self, nodes_from, nodes_to, results_raw,
                               resample_mode=None, agg_mode='sum'):
        """Aggregate raw data for each node in `nodes_from` to `nodes_to`.

        Either `nodes_from` or `nodes_to` must contain a single node
        label, the other one can contain one or more labels.

        Parameters
        ----------
        nodes_from : :obj:`list` of :obj:`str`
            Source node labels, e.g. ['bus_el']
        nodes_to : :obj:`list` of :obj:`str`
            Target node labels, e.g. ['gen_el_wind', 'gen_el_pv_ground']
        results_raw : :obj:`dict` of :pandas:`pandas.DataFrame`
            Raw result data from optimization as created by oemof
        resample_mode : :obj:`str` or None
            Resampling option according to :pandas:`pandas.DataFrame.resample`
            If None, no resampling takes place and `agg_mode` is not used.
            Examples: 'A' (year), 'M' (month)
            Default: None
        agg_mode : :obj:`str`
            Aggregation mode for resampling given in `resample_mode`,
            possible values: 'sum', 'mean'
            Default: 'sum'

        Returns
        -------
        :obj:`list` of :obj:`tuple`
            Sum of annual flow by source or target node,
            format: [('name_1', [value_11, ..., value_1n]),
                      ...,
                     ('name_n', [value_n1, ..., value_nn])]
        """

        # extract requested columns
        if len(nodes_to) == 1 and len(nodes_from) >= 1:
            ts = self.get_raw_results_df(results_raw)[[(n_from, nodes_to[0])
                                                       for n_from in nodes_from]]
            multiple_nodes = 'from'
        elif len(nodes_from) == 1 and len(nodes_to) >= 1:
            ts = self.get_raw_results_df(results_raw)[[(nodes_from[0], n_to)
                                                       for n_to in nodes_to]]
            multiple_nodes = 'to'
        else:
            raise ValueError('One of source and target nodes '
                             'must contain exactly 1 node, the '
                             'other >=1 nodes.')

        # resampling and aggregation
        if resample_mode is not None:
            if agg_mode == 'sum':
                agg_data = ts.resample(resample_mode).sum()
            elif agg_mode == 'mean':
                agg_data = ts.resample(resample_mode).mean()
            else:
                raise ValueError('Aggregation mode is invalid.')
        else:
            agg_data = ts

        # reformat
        if multiple_nodes == 'from':
            agg_data = [(NODE_LABELS[k[0]], [round(_/1000, 1) for _ in v])
                        for k, v in agg_data.to_dict(orient='list').items()]
        elif multiple_nodes == 'to':
            agg_data = [(NODE_LABELS[k[1]], [round(_/1000, 1) for _ in v])
                        for k, v in agg_data.to_dict(orient='list').items()]

        return agg_data


class ResultChart(object):
    """
    Scenarios are loaded, analyzed and visualized within this class
    """
    def __init__(self, setup_labels, type=None, data=None):
        self.setup_labels = setup_labels
        self.type = type
        self.data = data

    def visualize(self, **kwargs):
        if self.type == 'line':
            visualization = highcharts.HCTimeseries(
                data=self.data,
                setup_labels=self.setup_labels,
                style='display: inline-block',
                **kwargs
            )
        elif self.type == 'pie':
            visualization = highcharts.HCPiechart(
                data=self.data,
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
