import os
from configobj import ConfigObj

from wam import settings


# import configs
LAYER_AREAS_METADATA = ConfigObj(os.path.join(settings.BASE_DIR,
                                              'stemp_abw',
                                              'config',
                                              'layers_areas.cfg'))

LAYER_REGION_METADATA = ConfigObj(os.path.join(settings.BASE_DIR,
                                               'stemp_abw',
                                               'config',
                                               'layers_region.cfg'))

LAYER_DEFAULT_STYLES = ConfigObj(os.path.join(settings.BASE_DIR,
                                              'stemp_abw',
                                              'config',
                                              'layer_default_styles.cfg'))

ESYS_COMPONENTS_METADATA = ConfigObj(os.path.join(settings.BASE_DIR,
                                                  'stemp_abw',
                                                  'config',
                                                  'esys_components.cfg'))

ESYS_AREAS_METADATA = ConfigObj(os.path.join(settings.BASE_DIR,
                                             'stemp_abw',
                                             'config',
                                             'esys_areas.cfg'))

LABELS = ConfigObj(os.path.join(settings.BASE_DIR,
                                'stemp_abw',
                                'config',
                                'labels.cfg'))

MAP_DATA_CACHE_TIMEOUT = 60 * 60

# Mapping between UI control id and data in scenario data dict.
# The value can be string or list of strings. If a list is provided, the
# control value is calculated using the sum of scenario's data values
CONTROL_VALUES_MAP = {'sl_wind': 'gen_capacity_wind',
                      'sl_pv_roof':
                          ['gen_capacity_pv_roof_large',
                           'gen_capacity_pv_roof_small'],
                      'sl_pv_ground': 'gen_capacity_pv_ground',
                      'sl_bio': 'gen_capacity_bio',
                      'sl_conventional':
                          ['gen_capacity_combined_cycle',
                           'gen_capacity_steam_turbine',
                           'gen_capacity_sewage_landfill_gas'],
                      'sl_resid_save_el': 'resid_save_el',
                      'sl_crt_save_el': 'crt_save_el',
                      'sl_resid_pth': 'resid_pth',
                      'sl_crt_pth': 'crt_pth',
                      'sl_resid_save_th': 'resid_save_th',
                      'sl_crt_save_th': 'crt_save_th',
                      'sl_battery': 'battery',
                      'sl_dsm_resid': 'dsm_resid',
                      'sl_emobility': 'emobility',
                      'sl_dist_resid': 'dist_resid',
                      'cb_use_forest': 'use_forest',
                      'cb_use_ffh_areas': 'use_ffh_areas',
                      'cb_use_cult_areas': 'use_cult_areas',
                      'dd_repowering': 'repowering_scn'
                      }

RE_POT_CONTROLS = ['sl_dist_resid',
                   'cb_use_forest',
                   'cb_use_ffh_areas',
                   'cb_use_cult_areas']

NODE_LABELS = {'gen_el_wind': 'Windenergie',
               'gen_el_pv_roof': 'PV Dach',
               'gen_el_pv_ground': 'PV Freifläche',
               'gen_el_hydro': 'Wasserkraft',
               'shortage_el': 'Import'
               }

RE_POT_LAYER_ID_LIST = [str(_) for _ in range(1,7)]

SIMULATION_CFG = {'date_from': '2017-01-01 00:00:00',
                  'date_to': '2017-01-07 23:00:00',
                  'freq': '60min',
                  'solver': 'cbc',
                  'verbose': True,
                  'keepfiles': False
                  }
