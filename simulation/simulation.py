import pandas as pd
import oemof.solph as solph
from oemof import outputlib
from stemp_abw.app_settings import SIMULATION_CFG as SIM_CFG


def default_simulation_fct(esys=None):

    om = solph.Model(energysystem=esys)

    om.solve(solver=SIM_CFG['solver'],
             solve_kwargs={'tee': SIM_CFG['verbose'],
             'keepfiles': SIM_CFG['keepfiles']})
    results = outputlib.processing.results(om)

    parameters = outputlib.processing.parameter_as_dict(
            om, exclude_none=True)
    
    return map(
        outputlib.processing.convert_keys_to_strings,
        (results, parameters)
    )
