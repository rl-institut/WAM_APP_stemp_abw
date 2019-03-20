import pandas as pd

import oemof.solph as solph
from stemp_abw.dataio.load_static import load_timeseries, load_mun_data

TIMESERIES = load_timeseries()
MUN_DATA = load_mun_data()


def prepare_feedin_timeseries(mun_data):
    """Calculate capacity(mun)-weighted aggregated feedin timeseries per
    technology for entire region

    Returns
    -------
    :obj:`dict` of :obj:`list`
        Aggregated feedin timeseries
    """

    # needed columns from scenario's mun data for feedin
    cols = ['gen_capacity_wind',
            'gen_capacity_pv_ground',
            'gen_capacity_pv_roof_small',
            'gen_capacity_pv_roof_large',
            'gen_capacity_hydro']

    # mapping for RE capacity columns to RE timeseries columns
    tech_mapping = {'gen_capacity_wind': 'wind_sq',
                    'gen_capacity_pv_ground': 'pv_ground',
                    'gen_capacity_hydro': 'hydro'}

    # prepare RE capacities
    re_cap_per_mun = pd.DataFrame.from_dict(mun_data, orient='index')[cols]\
        .rename(columns=tech_mapping)
    re_cap_per_mun.index = re_cap_per_mun.index.astype(int)
    re_cap_per_mun['pv_roof'] = \
        re_cap_per_mun['gen_capacity_pv_roof_small'] + \
        re_cap_per_mun['gen_capacity_pv_roof_large']
    re_cap_per_mun.drop(columns=['gen_capacity_pv_roof_small',
                                 'gen_capacity_pv_roof_large'],
                        inplace=True)
    re_cap_per_mun['wind_fs'] = 0

    # calculate capacity(mun)-weighted aggregated feedin timeseries for entire region
    feedin_agg = {}
    for tech in list(re_cap_per_mun.columns):
        feedin_agg[tech] = list((TIMESERIES['feedin'][tech] * re_cap_per_mun[tech]).sum(axis=1))

    return feedin_agg


def prepare_demand_timeseries(mun_data):
    """Calculate aggregated feedin timeseries per sector for entire region

    Returns
    -------
    :obj:`dict` of :obj:`list`
        Aggregated feedin timeseries
    """

    # aggregated:
    demand_agg = TIMESERIES['demand'] \
        .sum(axis=1, level=0) \
        .to_dict(orient='list')

    return demand_agg


def create_nodes(mun_data, reg_params):

    feedin = prepare_feedin_timeseries(mun_data)
    demand = prepare_demand_timeseries(mun_data)

    # debug
    feedin_sum=0
    demand_sum=0
    for _ in feedin.keys():
        print(f'Feedin sum of {_}: ', sum(feedin[_]))
        feedin_sum += sum(feedin[_])
    for _ in demand.keys():
        print(f'Demand sum of {_}: ', sum(demand[_]))
        demand_sum += sum(demand[_])
    print('Total feedin sum: ', feedin_sum)
    print('Total demand sum: ', demand_sum)
    # debug end

    nodes = []

    bus_el = solph.Bus(label='bus_el', balanced=True)
    nodes.append(bus_el)

    # fixed sources (electrical)
    nodes.append(solph.Source(label='gen_el_wind',
                              outputs={bus_el: solph.Flow(nominal_value=1,
                                                          variable_costs=0,
                                                          actual_value=feedin['wind_sq'],
                                                          fixed=True
                                                          )})
                 )
    nodes.append(solph.Source(label='gen_el_pv_roof',
                              outputs={bus_el: solph.Flow(nominal_value=1,
                                                          variable_costs=0,
                                                          actual_value=feedin['pv_roof'],
                                                          fixed=True
                                                          )})
                 )
    nodes.append(solph.Source(label='gen_el_pv_ground',
                              outputs={bus_el: solph.Flow(nominal_value=1,
                                                          variable_costs=0,
                                                          actual_value=feedin['pv_ground'],
                                                          fixed=True
                                                          )})
                 )
    nodes.append(solph.Source(label='gen_el_hydro',
                              outputs={bus_el: solph.Flow(nominal_value=1,
                                                          variable_costs=0,
                                                          actual_value=feedin['hydro'],
                                                          fixed=True
                                                          )})
                 )

    # dispatchable sources (electrical and heat)
    # TBD

    # fixed demand (electrical)
    nodes.append(solph.Sink(label='dem_el_hh',
                            inputs={bus_el: solph.Flow(nominal_value=1,
                                                       actual_value=demand['el_hh'],
                                                       fixed=True
                                                       )})
                 )
    nodes.append(solph.Sink(label='dem_el_rca',
                            inputs={bus_el: solph.Flow(nominal_value=1,
                                                       actual_value=demand['el_rca'],
                                                       fixed=True
                                                       )})
                 )
    nodes.append(solph.Sink(label='dem_el_ind',
                            inputs={bus_el: solph.Flow(nominal_value=1,
                                                       actual_value=demand['el_ind'],
                                                       fixed=True
                                                       )})
                 )

    # excess and shortage (electrical)
    nodes.append(solph.Source(label='shortage_el',
                              outputs={bus_el: solph.Flow(variable_costs=100)})
                 )
    nodes.append(solph.Sink(label='excess_el',
                            inputs={bus_el: solph.Flow(variable_costs=200)})
                 )

    return nodes
