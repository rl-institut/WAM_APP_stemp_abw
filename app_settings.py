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

LABELS = ConfigObj(os.path.join(settings.BASE_DIR,
                                'stemp_abw',
                                'config',
                                'labels.cfg'))

MAP_DATA_CACHE_TIMEOUT = 60 * 60
