import json
from uuid import uuid4, UUID
import hashlib
import pandas as pd
import oemof.solph as solph
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from stemp_abw.models import Scenario, RepoweringScenario, ScenarioData
from stemp_abw.app_settings import CONTROL_VALUES_MAP
from stemp_abw.simulation.bookkeeping import simulate_energysystem
from stemp_abw.app_settings import SIMULATION_CFG as SIM_CFG
from stemp_abw.simulation.esys import create_nodes
from stemp_abw.results.results import Results
from stemp_abw.results.io import oemof_json_to_results


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
    tech_ratios : :pandas:`pandas.DataFrame<dataframe>`
        Capacity ratios of specific technologies in the region belonging to the
        same category from status quo scenario, for details see
        :meth:`stemp_abw.sessions.UserSession.create_reg_tech_ratios`
    tracker : :class:`stemp_abw.sessions.Tracker`
        Holds tool usage data

    Notes
    -----
    INSERT NOTES
    """
    def __init__(self):
        self.user_scenario = self.__scenario_to_user_scenario()
        self.simulation = Simulation(session=self)
        self.mun_to_reg_ratios = self.create_mun_data_ratio_for_aggregation()
        self.tech_ratios = self.create_reg_tech_ratios()
        self.tracker = Tracker(session=self)
        self.highcharts_temp = None

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
            # TODO: Use exists() instead
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
        # TODO: Save scenario
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

    @staticmethod
    def create_mun_data_ratio_for_aggregation():
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

    def update_scenario_data(self, ctrl_data=None):
        """Update municipal data of user scenario

        Parameters
        ----------
        ctrl_data : :obj:`dict`
            Data to update in the scenario, e.g. {'sl_wind': 500}

        Notes
        -----
        Keys of dictionary must be ids of UI controls (contained in mapping
        dict CONTROL_VALUES_MAP). According to this mapping dict, some params
        require changes of multiple entries in scenario data. This is done by
        capacity-proportional change of those entries (see 2 below).
        """
        if not isinstance(ctrl_data, dict) or len(ctrl_data) == 0:
            raise ValueError('Data dict not specified or empty!')

        reg_data_upd = {}

        # calculate new regional params
        for c_name, val in ctrl_data.items():
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
        for k, v in reg_data_upd.items():
            if k in scn_data['reg_params']:
                scn_data['reg_params'][k] = v
        # update municipal data
        for mun, v in self.__disaggregate_reg_to_mun_data(reg_data_upd).items():
            scn_data['mun_data'][mun].update(v)

        # updates at change of repowering scenario
        if 'dd_repowering' in ctrl_data:
            # 1) change repowering scn DB entry for scenario
            self.user_scenario.repowering_scenario = \
                RepoweringScenario.objects.get(
                    id=scn_data['reg_params']['repowering_scn'])
            # 2) mun data update
            # free sceario
            if int(ctrl_data['dd_repowering']) == -1:
                print(self.user_scenario)
                sl_wind_repower_pot = round(
                    sum([scn_data['mun_data'][mun]['gen_capacity_wind']
                         for mun in scn_data['mun_data'].keys()]
                        )
                )
            # other scenarios
            else:
                repower_data = json.loads(self.user_scenario.repowering_scenario.data)
                for mun in scn_data['mun_data']:
                    scn_data['mun_data'][mun]['gen_capacity_wind'] =\
                        repower_data[mun]['gen_capacity_wind']
                # 3) calculate potential for wind slider update
                sl_wind_repower_pot = \
                    round(sum([_['gen_capacity_wind']
                               for _ in repower_data.values()]))

        else:
            sl_wind_repower_pot = None

        self.user_scenario.data.data = json.dumps(scn_data,
                                                  sort_keys=True)

        return sl_wind_repower_pot

    def __disaggregate_reg_to_mun_data(self, reg_data):
        """Disaggregate given regional data to given municipal data
        
        Parameters
        ----------
        reg_data : :obj:`dict`
            Regional data (updated)
        """
        mun_data_upd = pd.DataFrame()
        for param in reg_data:
            if param in self.mun_to_reg_ratios.columns:
                mun_data_upd[param] = (self.mun_to_reg_ratios[param] *
                                       reg_data[param]).round(decimals=1)
        return mun_data_upd.to_dict(orient='index')

    # def __prepare_re_potential_


class Simulation(object):
    """Simulation data

    TODO: Finish docstring
    """
    def __init__(self, session):
        self.esys = None
        self.session = session
        self.results = Results(simulation=self)
        #self.create_esys()
        #self.load_or_simulate()
        #self.x = self.results.get_result_charts_data()
    
    def create_esys(self):
        """Create energy system, parametrize and add nodes"""

        # create esys
        self.esys = solph.EnergySystem(
            timeindex=pd.date_range(start=SIM_CFG['date_from'],
                                    end=SIM_CFG['date_to'],
                                    freq=SIM_CFG['freq']))
        # create nodes from user scenario and add to energy system
        self.esys.add(*create_nodes(**json.loads(self.session.user_scenario.data.data)))

    def load_or_simulate(self):
        """Load results from DB if existing, start simulation if not

        Check if results are already in the DB using Scenario data's UUID
        """
        user_scn_data_uuid = UUID(hashlib.md5(
            self.session.user_scenario.data.data.encode('utf-8')).hexdigest())

        # reverse lookup for scenario
        if Scenario.objects.filter(data__data_uuid=user_scn_data_uuid).exists():
            print('Scenario results found, load from DB...')
            results_json = Scenario.objects.get(
                data__data_uuid=user_scn_data_uuid).results.data
            self.store_values(*oemof_json_to_results(results_json))
        else:
            print('Scenario results not found, start simulation...')
            self.store_values(*simulate_energysystem(self.esys))

    def store_values(self, results, param_results):
        # update result raw data
        self.results.set_result_raw_data(results_raw=results,
                                         param_results_raw=param_results)
        # TODO: save results


class Tracker(object):
    """Tracker to store certain user activity

    E.g. to show popups for features if the user has not visited a certain
    part in the session.
    """
    def __init__(self, session):
        self.session = session
        self.visited = self.__init_data()

    def __init_data(self):
        visited = {'esys': False,
                   'areas': False}
        return visited
