import pandas as pd
import oemof.solph as solph
from oemof import outputlib
from stemp_abw.simulation.esys import energy_system
from numpy.random import random


def default_simulation_fct():
    cfg = {
        'date_from': '2017-01-01 00:00:00',
        'date_to': '2017-01-31 23:00:00',
        'freq': '60min',
        'solver': 'cbc',
        'verbose': True,
        'keepfiles': False
    }

    datetime_index = pd.date_range(start=cfg['date_from'],
                                   end=cfg['date_to'],
                                   freq=cfg['freq'])

    esys_config = {
        'gen_capacity_wind': 650,
        'gen_capacity_pv_ground': 300,
        'gen_capacity_pv_roof': 160,
        'gen_capacity_hydro': 3,
        'gen_capacity_bio': 100,
        'gen_capacity_conv': 225
    }

    # create and parametrize esys
    esys = energy_system(datetime_index, esys_config)

    om = solph.Model(energysystem=esys)

    om.solve(solver=cfg['solver'],
             solve_kwargs={'tee': cfg['verbose'],
             'keepfiles': cfg['keepfiles']})
    results = outputlib.processing.results(om)

    parameters = outputlib.processing.parameter_as_dict(
            om, exclude_none=True)
    
    return map(
        outputlib.processing.convert_keys_to_strings,
        (results, parameters)
    )
