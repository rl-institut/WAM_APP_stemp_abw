import pandas as pd
import oemof.solph as solph
from oemof import outputlib
from numpy.random import random


def simulation_fct_test():
    cfg = {
        'date_from': '2016-02-01 00:00:00',
        'date_to': '2016-02-01 03:00:00',
        'freq': '60min',
        'solver': 'cbc',
        'verbose': True
    }

    datetime_index = pd.date_range(start=cfg['date_from'],
                                   end=cfg['date_to'],
                                   freq=cfg['freq'])

    feedin_el = random(len(datetime_index))
    demand_el = random(len(datetime_index))

    esys = solph.EnergySystem(timeindex=datetime_index)

    nodes = []
    bus_el = solph.Bus(label='bus_el')
    nodes.append(bus_el)

    nodes.append(solph.Source(label='wind',
                              outputs={bus_el: solph.Flow(nominal_value=10,
                                                          variable_costs=1,
                                                          actual_value=feedin_el,
                                                          fixed=True
                                                          )})
                 )
    nodes.append(solph.Source(label='bus_el_shortage',
                              outputs={bus_el: solph.Flow(variable_costs=100)})
                 )
    nodes.append(solph.Sink(label='bus_el_excess',
                            inputs={bus_el: solph.Flow(variable_costs=200)})
                 )

    nodes.append(solph.Sink(label='demand_el',
                            inputs={bus_el: solph.Flow(nominal_value=10,
                                                       actual_value=demand_el,
                                                       fixed=True
                                                       )})
                 )

    esys.add(*nodes)


    om = solph.Model(energysystem=esys)

    om.solve(solver=cfg['solver'],
             solve_kwargs={'tee': cfg['verbose'],
             'keepfiles': False})
    results = outputlib.processing.results(om)

    param_results = outputlib.processing.parameter_as_dict(
            om, exclude_none=True)
    return map(
        outputlib.processing.convert_keys_to_strings,
        (results, param_results)
    )


# class Simulation(object):
#
#     def __init__(self):
#         self.cfg = {
#             'date_from': '2016-02-01 00:00:00',
#             'date_to': '2016-02-01 23:00:00',
#             'freq': '60min',
#             'solver': 'cbc',
#             'verbose': True
#         }
#
#         datetime_index = pd.date_range(start=self.cfg['date_from'],
#                                        end=self.cfg['date_to'],
#                                        freq=self.cfg['freq'])
#
#         feedin_el = random(len(datetime_index))
#         demand_el = random(len(datetime_index))
#
#         self.esys = solph.EnergySystem(timeindex=datetime_index)
#
#
#         nodes = []
#         bus_el = solph.Bus(label='bus_el')
#         nodes.append(bus_el)
#
#         nodes.append(solph.Source(label='wind',
#                                   outputs={bus_el: solph.Flow(nominal_value=10,
#                                                               variable_costs=1,
#                                                               actual_value=feedin_el,
#                                                               fixed=True
#                                                               )})
#                      )
#         nodes.append(solph.Source(label='bus_el_shortage',
#                                   outputs={bus_el: solph.Flow(variable_costs=100)})
#                      )
#         nodes.append(solph.Sink(label='bus_el_excess',
#                                 inputs={bus_el: solph.Flow(variable_costs=200)})
#                      )
#
#         nodes.append(solph.Sink(label='demand_el',
#                                 inputs={bus_el: solph.Flow(nominal_value=10,
#                                                            actual_value=demand_el,
#                                                            fixed=True
#                                                            )})
#                      )
#
#         self.esys.add(*nodes)
#
#
#     def run(self):
#         optimization_model = solph.Model(energysystem=self.esys)
#
#         optimization_model.solve(solver=self.cfg['solver'],
#                                  solve_kwargs={'tee': self.cfg['verbose'],
#                                                'keepfiles': False})
#         optimization_model.results()
#
#         results = optimization_model.results()
#
#         # for bus in (bus_el,):
#         #     # get bus from results
#         #     bus_results = views.node(results, bus.label)
#         #     bus_results_flows = bus_results['sequences']
#         #
#         #     # print some sums for bus
#         #     print(bus_results['sequences'].sum())
#         #     print(bus_results['sequences'].info())
#         return results
