import json
from uuid import uuid4
import pandas as pd
import oemof.solph as solph
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from stemp_abw.models import Scenario
from stemp_abw.app_settings import CONTROL_VALUES_MAP
from stemp_abw.simulation.bookkeeping import simulate_energysystem
from stemp_abw.app_settings import SIMULATION_CFG as SIM_CFG
from stemp_abw.simulation.esys import create_nodes


class UserSession(object):
    def __init__(self):
        self.user_scenario = self.__scenario_to_user_scenario()
        self.simulation = Simulation(session=self)
        
    @property
    def scenarios(self):
        return {scn.id: scn
                for scn in Scenario.objects.filter(
                    is_user_scenario=False).all()
                }
        
    def __scenario_to_user_scenario(self, scn_id=None):
        """Make a copy of a scenario and return as user scenario

        At startup, use status quo scenario as user scenario. This may change
        when a different scenario is applied in the tool (apply button).

        Parameters
        ----------
        scn_id : obj:`int`
          id of scenario. If not provided, status quo scenario from DB is used
        """
        if scn_id is None:
            try:
                scn = Scenario.objects.get(name='Status quo')
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist('Szenario "Status quo" nicht gefunden!')
        else:
            scn = self.scenarios[int(scn_id)]
        scn.name = 'User Scenario {uuid}'.format(uuid=str(uuid4()))
        scn.description = ''
        scn.id = None
        scn.is_user_scenario = True
        scn.created = timezone.now()
        # scn.save()
        return scn
    
    def set_user_scenario(self, scn_id):
        """Set user scenario to scenario from DB
        
        Parameters
        ----------
        scn_id : :obj:`int`
          id of scenario
        """
        self.user_scenario = self.__scenario_to_user_scenario(scn_id=scn_id)

    @staticmethod
    def get_control_values(scenario):
        """Returns a JSON with values for the UI controls (e,g, sliders)

        Parameters
        ----------
        scenario : :class:`stemp_abw.models.Scenario`
            Scenario to read data from

        Notes
        -----
        Data is taken from user scenario, CONTROL_VALUES_MAP defines the
        mapping from controls' ids to the data entry.
        """
        scn_data = json.loads(scenario.data.data)

        # build value dict mapping between control id and data in scenario data dict
        control_values = {}
        for c_name, d_name in CONTROL_VALUES_MAP.items():
            if isinstance(CONTROL_VALUES_MAP[c_name], str):
                control_values[c_name] = scn_data['reg_data'][d_name]
            elif isinstance(CONTROL_VALUES_MAP[c_name], list):
                control_values[c_name] = sum([scn_data['reg_data'][d_name_2]
                                              for d_name_2
                                              in CONTROL_VALUES_MAP[c_name]])
        return control_values

    def update_scenario_data(self, data=None):
        """Updates the regional parameters of the user scenario

        Parameters
        ----------
        data : :obj:`dict`
            Data to update in the scenario, e.g. {'sl_wind': 500}

        Notes
        -----
        Keys of dictionary must be ids of UI controls (contained in
        CONTROL_VALUES_MAP).
        """
        if not isinstance(data, dict) or len(data) == 0:
            raise ValueError('Data dict not specified or empty!')
        
        scn_data = json.loads(self.user_scenario.data.data)
        for c_name, val in data.items():
            if isinstance(CONTROL_VALUES_MAP[c_name], str):
                scn_data['reg_data'][c_name] = val
            elif isinstance(CONTROL_VALUES_MAP[c_name], list):
                val_sum = sum([scn_data['reg_data'][d_name]
                               for d_name in CONTROL_VALUES_MAP[c_name]])
                for d_name in CONTROL_VALUES_MAP[c_name]:
                    scn_data['reg_data'][d_name] = \
                        val * scn_data['reg_data'][d_name] / val_sum

        self.user_scenario.data.data = json.dumps(scn_data,
                                                  sort_keys=True)


class Simulation(object):
    def __init__(self, session):
        self.esys = None
        self.session = session
        #self.create_esys()
        #self.simulate()
    
    def create_esys(self):
        # create esys
        self.esys = solph.EnergySystem(
            timeindex=pd.date_range(start=SIM_CFG['date_from'],
                                    end=SIM_CFG['date_to'],
                                    freq=SIM_CFG['freq']))
        self.esys.add(*create_nodes(**json.loads(self.session.user_scenario.data.data)))
    
    def simulate(self):
        self.store_values(*simulate_energysystem(self.esys))

    def store_values(self, results, param_results):
        print('Results:', results)
        print('Params:', param_results)