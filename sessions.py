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
    """User session

    Attributes
    ----------
    user_scenario : :class:`stemp_abw.models.Scenario`
        User's scenario (data updated continuously during tool operation)
    simulation : :class:`stemp_abw.sessions.Simulation`
        Holds data related to energy system
    mun_to_reg_ratios : :obj:`dict`
        Capacity ratios of municipality to regional values, for details see
        :meth:`stemp_abw.sessions.UserSession.create_mun_data_ratio_for_aggregation`
    mun_to_reg_ratios : :pandas:`pandas.DataFrame<dataframe>`
        Capacity ratios of specific technologies in the region belonging to the
        same category from status quo scenario, for details see
        :meth:`stemp_abw.sessions.UserSession.create_reg_tech_ratios`

    Notes
    -----
    INSERT NOTES
    """
    def __init__(self):
        self.user_scenario = self.__scenario_to_user_scenario()
        self.simulation = Simulation(session=self)
        self.mun_to_reg_ratios = self.create_mun_data_ratio_for_aggregation()
        self.tech_ratios = self.create_reg_tech_ratios()

    @property
    def scenarios(self):
        """Return all default scenarios (not created by user)"""
        return {scn.id: scn
                for scn in Scenario.objects.filter(
                    is_user_scenario=False).all()
                }

    @property
    def region_data(self):
        """Aggregate municipal data and return region data for user scenario

        Notes
        -----
        Also includes regional params contained in scenario.
        """
        return self.region_data_for_scenario(self.user_scenario)

    def region_data_for_scenario(self, scenario):
        """Aggregate municipal data and return region data for given scenario

        Notes
        -----
        Also includes regional params contained in scenario.
        """
        scn_data = json.loads(scenario.data.data)
        reg_data = pd.DataFrame.from_dict(scn_data['mun_data'],
                                          orient='index'). \
            sum(axis=0).round(decimals=1).to_dict()
        reg_data.update(scn_data['reg_params'])
        return reg_data
        
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

    def get_control_values(self, scenario):
        """Return a JSON with values for the UI controls (e,g, sliders)
        for a given scenario.

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
        reg_data = self.region_data_for_scenario(scenario)

        # build value dict mapping between control id and data in scenario data dict
        control_values = {}
        for c_name, d_name in CONTROL_VALUES_MAP.items():
            if isinstance(CONTROL_VALUES_MAP[c_name], str):
                control_values[c_name] = reg_data[d_name]
            elif isinstance(CONTROL_VALUES_MAP[c_name], list):
                control_values[c_name] = sum([reg_data[d_name_2]
                                              for d_name_2
                                              in CONTROL_VALUES_MAP[c_name]])
        return control_values

    def create_mun_data_ratio_for_aggregation(self):
        """Create table of technology shares for municipalities from status
        quo scenario.

        The scenario holds data for every municipality. In contrast, the UI
        uses values for the entire region. Hence, the capacity ratio of a
        certain parameter between municipality and entire region is needed for
        aggregation (mun->region) or disaggragation (region->mun).
        An instantaneous calculation is inappropriate as it leads to error
        propagation.
        """
        scn = Scenario.objects.get(name='Status quo')
        scn_data = pd.DataFrame.from_dict(
            json.loads(scn.data.data)['mun_data'],
            orient='index')
        return scn_data / scn_data.sum(axis=0)

    def create_reg_tech_ratios(self):
        """Create table with share of specific technologies belonging to the
        same category from status quo scenario.

        The scenario holds data for specific sub-technonogies. In contrast,
        the UI uses values for a superior technology (e.g. 'pv_roof' is split
        into 'gen_capacity_pv_roof_large' and 'gen_capacity_pv_roof_small').
        Hence, the capacity ratio of a certain sub-technology and its superior
        technology is needed to determine when mapping between these two data
        models.
        An instantaneous calculation is inappropriate as it leads to error
        propagation.
        """
        reg_data = self.region_data_for_scenario(
            Scenario.objects.get(name='Status quo'))
        tech_ratios = {}
        # find needed params for the mapping
        for c_name, d_name in CONTROL_VALUES_MAP.items():
            if isinstance(d_name, list):
                for subtech in d_name:
                    tech_ratios[subtech] = reg_data[subtech] /\
                                           sum([reg_data[_] for _ in d_name])
        return tech_ratios

    def update_scenario_data(self, data=None):
        """Update municipal data of user scenario

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

        reg_data = self.region_data
        reg_data_upd = {}

        # calculate new regional params
        for c_name, val in data.items():
            # 1) value to be set refers to a single entry (e.g. 'sl_wind')
            if isinstance(CONTROL_VALUES_MAP[c_name], str):
                reg_data_upd[CONTROL_VALUES_MAP[c_name]] = val
            # 2) value to be set refers to a list of entries (e.g. a change of
            # 'sl_pv_roof' needs changes of 'gen_capacity_pv_roof_large' and
            # 'gen_capacity_pv_roof_small')
            elif isinstance(CONTROL_VALUES_MAP[c_name], list):
                for d_name in CONTROL_VALUES_MAP[c_name]:
                    reg_data_upd[d_name] = val * self.tech_ratios[d_name]


        scn_data = json.loads(self.user_scenario.data.data)
        # update regional data
        scn_data['reg_params'].update(reg_data_upd)
        # update municipal data
        for mun, data in self.__disaggregate_reg_to_mun_data(reg_data_upd).items():
            scn_data['mun_data'][mun].update(data)

        self.user_scenario.data.data = json.dumps(scn_data,
                                                  sort_keys=True)

    def __disaggregate_reg_to_mun_data(self, reg_data):
        """Disaggregate given regional data to given municipal data
        
        Parameters
        ----------
        reg_data : :obj:`dict`
            Regional data (updated)
        """
        mun_data_upd = pd.DataFrame()
        for param in reg_data.keys():
            if param in self.mun_to_reg_ratios.columns:
                mun_data_upd[param] = (self.mun_to_reg_ratios[param] *
                                       reg_data[param]).round(decimals=1)
        return mun_data_upd.to_dict(orient='index')


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
        # create nodes from user scenario and add o energy system
        self.esys.add(*create_nodes(**json.loads(self.session.user_scenario.data.data)))
    
    def simulate(self):
        self.store_values(*simulate_energysystem(self.esys))

    def store_values(self, results, param_results):
        #print('Results:', results)
        #print('Params:', param_results)
        pass