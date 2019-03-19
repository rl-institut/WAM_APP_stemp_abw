import json
from uuid import uuid4
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from stemp_abw.models import Scenario


class UserSession(object):
    def __init__(self):
        self.user_scenario = self.__scenario_to_user_scenario()
        self.simulation = Simulation()
        #self.xxx = self.get_control_values(self.user_scenario)

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
    
    def update_user_scenario(self, scn_id):
        """Set user scenario to scenario from DB
        
        Parameters
        ----------
        scn_id : obj:`int`
          id of scenario
        """
        self.user_scenario = self.__scenario_to_user_scenario(scn_id=scn_id)

    @staticmethod
    def get_control_values(scenario):
        """Returns a JSON with values for the UI controls (e,g, sliders)"""
        scn_data = json.loads(scenario.data.data)

        # region_mapping = {'sl_wind': 'gen_capacity_wind',
        #                   'sl_pv_roof': }
        reg_data = scn_data['region_data']
        global_params = scn_data['global_params']
        control_values = {'sl_wind': reg_data['gen_capacity_wind'],
                          'sl_pv_roof':
                              reg_data['gen_capacity_pv_roof_large'] +
                              reg_data['gen_capacity_pv_roof_small'],
                          'sl_pv_ground': reg_data['gen_capacity_pv_ground'],
                          'sl_bio': reg_data['gen_capacity_bio'],
                          'sl_conventional':
                              reg_data['gen_capacity_combined_cycle'] +
                              reg_data['gen_capacity_steam_turbine'] +
                              reg_data['gen_capacity_sewage_landfill_gas'],
                          'sl_resid_save_el': global_params['resid_save_el'],
                          'sl_crt_save_el': global_params['crt_save_el'],
                          'sl_resid_pth': global_params['resid_pth'],
                          'sl_crt_pth': global_params['crt_pth'],
                          'sl_resid_save_th': global_params['resid_save_th'],
                          'sl_crt_save_th': global_params['crt_save_th'],
                          'sl_battery': global_params['battery'],
                          'sl_dsm_resid': global_params['dsm_resid'],
                          'sl_emobility': global_params['emobility'],
                          'sl_dist_resid': global_params['dist_resid'],
                          'cb_use_forest': global_params['use_forest'],
                          'cb_use_ffh_areas': global_params['use_ffh_areas'],
                          'cb_use_cult_areas': global_params['use_cult_areas']
                          }
        return control_values


class Simulation(object):
    def __init__(self):
        self.esys = None
