import os
from collections import OrderedDict
import sqlalchemy
import sqlahelper
from configobj import ConfigObj

import oedialect as _

from wam import settings
#from db_apps import oemof_results
from stemp_abw import oep_models

# SCENARIO_PATH = os.path.join('stemp', 'scenarios')

# ADDITIONAL_PARAMETERS = ConfigObj(
#     os.path.join(settings.BASE_DIR, 'stemp', 'attributes.cfg'))


DB_URL = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}'


def build_db_url(db_name):
    conf = settings.config['DATABASES'][db_name]
    #conf['ENGINE'] = 'postgresql+oedialect'
    db_url = DB_URL + '/{NAME}' if 'NAME' in conf else DB_URL
    return db_url.format(**conf)


# # Add sqlalchemy for oemof_results:
# engine = sqlalchemy.create_engine(build_db_url('DEFAULT'))
# sqlahelper.add_engine(engine, 'oemof_results')
# oemof_results.Base.metadata.bind = engine

# # Add local DB:
# engine = sqlalchemy.create_engine(build_db_url('DEFAULT'))
# sqlahelper.add_engine(engine, 'lokal')
# oep_models.Base.metadata.bind = engine

# # Add OEP:
# engine = sqlalchemy.create_engine(build_db_url('OEP'))
# sqlahelper.add_engine(engine, 'oep')
# oep_models.Base.metadata.bind = engine

# # Add reiner:
# engine = sqlalchemy.create_engine(build_db_url('reiners_db'))
# sqlahelper.add_engine(engine, 'reiners_db')

# TODO: Verify configs after import / make failsafe!
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

SIMULATION_CFG = {'date_from': '2017-01-01 00:00:00',
                  'date_to': '2017-01-07 23:00:00',
                  'freq': '60min',
                  'solver': 'cbc',
                  'verbose': True,
                  'keepfiles': False
                  }
