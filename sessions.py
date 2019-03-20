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
        """Return a JSON with values for the UI controls (e,g, sliders)

        Parameters
        ----------
        scenario : :class:`stemp_abw.models.Scenario`
            Scenario to read data from

        Notes
        -----
        Data is taken from aggregated regional data of user scenario,
        CONTROL_VALUES_MAP defines the mapping from controls' ids to the data
        entry.
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
        """Update parameters of user scenario

        Parameters
        ----------
        data : :obj:`dict`
            Data to update in the scenario, e.g. {'sl_wind': 500}

        Notes
        -----
        Keys of dictionary must be ids of UI controls (contained in mapping
        dict CONTROL_VALUES_MAP). According to this mapping dict, some params
        require changes of multiple entries in scenario data. This is done by
        capacity-proportional change of those entries (see 2 below).
        """
        if not isinstance(data, dict) or len(data) == 0:
            raise ValueError('Data dict not specified or empty!')

        # update regional params
        scn_data = json.loads(self.user_scenario.data.data)
        for c_name, val in data.items():
            # 1) value to be set refers to a single entry (e.g. 'sl_wind')
            if isinstance(CONTROL_VALUES_MAP[c_name], str):
                scn_data['reg_data'][CONTROL_VALUES_MAP[c_name]] = val
            # 2) value to be set refers to a list of entries (e.g. a change of
            # 'sl_pv_roof' needs changes of 'gen_capacity_pv_roof_large' and
            # 'gen_capacity_pv_roof_small')
            elif isinstance(CONTROL_VALUES_MAP[c_name], list):
                val_sum = sum([scn_data['reg_data'][d_name]
                               for d_name in CONTROL_VALUES_MAP[c_name]])
                for d_name in CONTROL_VALUES_MAP[c_name]:
                    scn_data['reg_data'][d_name] = \
                        val * scn_data['reg_data'][d_name] / val_sum

        # update municipal params
        scn_data['mun_data'].update(
            self.__disaggregate_reg_to_mun_data(scn_data))

        self.user_scenario.data.data = json.dumps(scn_data,
                                                  sort_keys=True)

    def __disaggregate_reg_to_mun_data(self, scn_data):
        """Disaggregate regional data to municipal data in user scenario"""
        # for mun_param in next(iter(scn_data['mun_data'].values())).keys():
        mun_data = pd.DataFrame.from_dict(scn_data['mun_data'], orient='index')
        mun_data2 = mun_data.copy()
        for param in list(mun_data.columns):
            mun_data[param] = (mun_data[param] *
                               (scn_data['reg_data'][param] /
                                mun_data[param].sum(axis=0))).round(decimals=1)
        return mun_data.to_dict(orient='index')


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