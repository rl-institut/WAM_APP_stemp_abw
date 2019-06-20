from stemp_abw.visualizations import highcharts
from stemp_abw.models import Scenario, RegMun, MunData
from stemp_abw.results.io import oemof_json_to_results
from stemp_abw.app_settings import NODE_LABELS, SIMULATION_CFG as SIM_CFG
from stemp_abw.config.io import LABEL_DATA

from oemof.outputlib import views

import pandas as pd
import json


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
        nodes_from_prod = ['gen_el_wind',
                           'gen_el_pv_ground',
                           'gen_el_pv_roof',
                           'gen_el_hydro',
                           'gen_el_bio',
                           'gen_el_conventional',
                           'shortage_el']
        nodes_to_prod = ['bus_el']

        # 1) Annual data (user scenario + SQ)
        #####################################
        # aggregate raw data
        data_power_prod_a_user_scn = self.aggregate_flow_results(
            nodes_from_prod,
            nodes_to_prod,
            self.results_raw,
            resample_mode='A',
            agg_mode='sum'
        )
        data_power_prod_a_sq_scn = self.aggregate_flow_results(
            nodes_from_prod,
            nodes_to_prod,
            self.sq_results_raw,
            resample_mode='A',
            agg_mode='sum'
        )

        # prepare chart data
        hc_column_power_prod_both_scn = [{'name': k1, 'data': [v1[0], v2[0]]}
                                         for (k1, v1), (k2, v2) in
                                         zip(data_power_prod_a_user_scn,
                                             data_power_prod_a_sq_scn)]

        hc_pie_power_production_user_scn = [{'name': k, 'y': v[0]}
                                            for (k, v) in data_power_prod_a_user_scn]
        hc_pie_power_production_sq_scn = [{'name': k, 'y': v[0]}
                                          for (k, v) in data_power_prod_a_sq_scn]

        # 2) Monthly data (user scenario)
        #################################
        data_power_prod_m_user_scn = self.aggregate_flow_results(
            nodes_from=['gen_el_wind',
                        'gen_el_pv_ground',
                        'gen_el_pv_roof',
                        'gen_el_hydro',
                        'gen_el_bio'],
            nodes_to=['bus_el'],
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
        nodes_from_dem = ['bus_el']
        nodes_to_dem = ['dem_el_hh',
                        'dem_el_rca',
                        'dem_el_ind',
                        'excess_el']

        # aggregate raw data
        data_power_dem_a_user_scn = self.aggregate_flow_results(
            nodes_from_dem,
            nodes_to_dem,
            self.results_raw,
            resample_mode='A',
            agg_mode='sum'
        )
        data_power_dem_a_sq_scn = self.aggregate_flow_results(
            nodes_from_dem,
            nodes_to_dem,
            self.sq_results_raw,
            resample_mode='A',
            agg_mode='sum'
        )

        # prepare chart data
        hc_column_power_dem_both_scn = [{'name': k1, 'data': [v1[0], v2[0]]}
                                        for (k1, v1), (k2, v2) in
                                        zip(data_power_dem_a_user_scn,
                                            data_power_dem_a_sq_scn)]

        ###################
        # Own consumption #
        ###################

        # 1) column 1: balance
        ######################
        data_power_prod_a_user_scn_sum = sum([v[0] for (k,v)
                                            in data_power_prod_a_user_scn
                                            if k != 'Import'])
        data_power_prod_a_sq_scn_sum = sum([v[0] for (k, v)
                                          in data_power_prod_a_sq_scn
                                          if k != 'Import'])
        data_power_dem_a_user_scn_sum = sum([v[0] for (k,v)
                                           in data_power_dem_a_user_scn
                                           if k != 'Export'])
        data_power_dem_a_sq_scn_sum = sum([v[0] for (k, v)
                                         in data_power_dem_a_sq_scn
                                         if k != 'Export'])

        # prepare chart data
        hc_column_power_own_cons_both_scn_balance = [
            round(data_power_prod_a_user_scn_sum /
                  data_power_dem_a_user_scn_sum * 100, 1),
            round(data_power_prod_a_sq_scn_sum /
                  data_power_dem_a_sq_scn_sum * 100, 1)]

        # 2) column 2: simultaneous
        ###########################
        # production
        nodes_from = ['gen_el_wind',
                      'gen_el_pv_ground',
                      'gen_el_pv_roof',
                      'gen_el_hydro',
                      'gen_el_bio',
                      'gen_el_conventional']
        nodes_to = ['bus_el']
        data_power_prod_user_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            results_raw=self.results_raw
        ).sum(axis=1)
        data_power_prod_sq_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            self.sq_results_raw
        ).sum(axis=1)

        # demand
        nodes_from = ['bus_el']
        nodes_to = ['dem_el_hh',
                    'dem_el_rca',
                    'dem_el_ind']
        data_power_dem_a_user_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            self.results_raw
        ).sum(axis=1)
        data_power_dem_a_sq_scn = self.aggregate_flow_results(
            nodes_from,
            nodes_to,
            self.sq_results_raw
        ).sum(axis=1)

        # calc time share where prod >= demand
        data_power_prod_both_scn_simult = [
            round(sum(data_power_prod_user_scn >= data_power_dem_a_user_scn) /
                  len(data_power_prod_user_scn) * 100, 1),
            round(sum(data_power_prod_sq_scn >= data_power_dem_a_sq_scn) /
                  len(data_power_prod_sq_scn) * 100, 1)]

        # prepare chart data
        hc_column_power_own_cons_both_scn = [
            {'name': 'Bilanziell',
             'data': hc_column_power_own_cons_both_scn_balance},
            {'name': 'Zeitgleich',
             'data': data_power_prod_both_scn_simult}]

        ######################
        # make dict for json #
        ######################
        chart_data = {
            'hc_column_power_prod_both_scn':
                hc_column_power_prod_both_scn,
            'hc_column_power_dem_both_scn':
                hc_column_power_dem_both_scn,
            'hc_column_power_own_cons_both_scn':
                hc_column_power_own_cons_both_scn,
            'hc_pie_power_production_user_scn':
                hc_pie_power_production_user_scn,
            'hc_pie_power_production_sq_scn':
                hc_pie_power_production_sq_scn,
            'hc_column_power_prod_m_user_scn':
                hc_column_power_prod_m_user_scn,
            'hc_res_wind_time':
                [5, 5, 5, 4, 2, 0, 2, 8, 1, 7, 1]
        }

        return chart_data

    def get_layer_results(self):
        """Analyze results and return data for layer display"""

        # get user scn results for muns
        scn_data = json.loads(self.simulation.session.user_scenario.data.data)
        mun_results = pd.DataFrame.from_dict(scn_data['mun_data'],
                                          orient='index')
        mun_results.index = mun_results.index.astype(int)
        mun_data = pd.DataFrame(list(
            MunData.objects \
                .values_list('ags', 'area', named=True))).set_index(['ags'])
        mun_data.index = mun_data.index.astype(int)

        results = pd.DataFrame(list(
            RegMun.objects \
                .values_list('ags', named=True))).set_index(['ags'])

        # create DF with properties equivalent to those defined in models.py
        results['pop'] = mun_results['pop']
        results['pop_density'] = (
                mun_results['pop'] / mun_data['area']).round()

        results['gen_energy_re'] = (mun_results[[
            'gen_el_energy_wind',
            'gen_el_energy_pv_roof',
            'gen_el_energy_pv_ground',
            'gen_el_energy_hydro',
            'gen_el_energy_bio']].sum(axis=1) / 1e3).round()
        results['dem_el_energy'] = (mun_results[[
            'dem_el_energy_hh',
            'dem_el_energy_rca',
            'dem_el_energy_ind']].sum(axis=1) / 1e3).round()
        results['energy_re_el_dem_share'] = (
                results['gen_energy_re'] / results['dem_el_energy'] * 100).round()
        results['gen_energy_re_per_capita'] = (
                results['gen_energy_re'] / results['pop']).round(decimals=1)
        results['gen_energy_re_density'] = (
                results['gen_energy_re'] * 1e3 / mun_data['area']).round(decimals=1)

        results['gen_cap_re'] = (mun_results[[
            'gen_capacity_wind',
            'gen_capacity_pv_roof_large',
            'gen_capacity_pv_ground',
            'gen_capacity_hydro',
            'gen_capacity_bio']].sum(axis=1)).round()
        results['gen_cap_re_density'] = (
                results['gen_cap_re'] / mun_data['area']).round(decimals=2)

        results['gen_count_wind_density'] = (
                mun_results['gen_count_wind'] / mun_data['area']).round(decimals=2)
        results['dem_el_energy_per_capita'] = (
                results['dem_el_energy'] * 1e6 / results['pop']).round()

        results['dem_th_energy'] = (mun_results[[
            'dem_th_energy_hh',
            'dem_th_energy_rca']].sum(axis=1) / 1e3).round()
        results['dem_th_energy_per_capita'] = (
                results['dem_th_energy'] / results['pop']).round()
        results = results.add_suffix(suffix='_result')

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
        * If `resample_mode` is None:
            :pandas:`pandas.DataFrame` with raw timeseries
        * If `resample_mode` is not None:
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
            return ts

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
        # load tooltip text from labels using container id
        container_id = kwargs.get('renderTo', None)
        if container_id is not None:
            tooltip_section = LABEL_DATA['charts'].get(container_id, None)
            if tooltip_section is not None:
                tooltip_text = tooltip_section.get('text', '')
            else:
                tooltip_text = ''
        else:
            tooltip_text = ''

        # prepare chart
        if self.type == 'line':
            visualization = highcharts.HCTimeseries(
                data=self.data,
                setup_labels=self.setup_labels,
                tooltip_text=tooltip_text,
                style='display: inline-block',
                **kwargs
            )
        elif self.type == 'pie':
            visualization = highcharts.HCPiechart(
                data=self.data,
                setup_labels=self.setup_labels,
                tooltip_text=tooltip_text,
                style='display: inline-block',
                **kwargs
            )
        elif self.type == 'column':
            visualization = highcharts.HCStackedColumn(
                data=self.data,
                setup_labels=self.setup_labels,
                tooltip_text=tooltip_text,
                style='display: inline-block',
                **kwargs
            )
        else:
            raise ValueError

        return visualization
