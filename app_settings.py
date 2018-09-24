
# import os
import sqlalchemy
import sqlahelper
# from configobj import ConfigObj

import oedialect as _

from wam import settings
#from db_apps import oemof_results
from stemp_abw import oep_models

# SCENARIO_PATH = os.path.join('stemp', 'scenarios')

# ADDITIONAL_PARAMETERS = ConfigObj(
#     os.path.join(settings.BASE_DIR, 'stemp', 'attributes.cfg'))

# LABELS = ConfigObj(os.path.join(settings.BASE_DIR, 'stemp', 'labels.cfg'))

DB_URL = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}'


def build_db_url(db_name):
    conf = settings.config['DATABASES'][db_name]
    conf['ENGINE'] = 'postgresql+oedialect'
    db_url = DB_URL + '/{NAME}' if 'NAME' in conf else DB_URL
    return db_url.format(**conf)


# # Add sqlalchemy for oemof_results:
# engine = sqlalchemy.create_engine(build_db_url('DEFAULT'))
# sqlahelper.add_engine(engine, 'oemof_results')
# oemof_results.Base.metadata.bind = engine

# Add local DB:
engine = sqlalchemy.create_engine(build_db_url('DEFAULT'))
sqlahelper.add_engine(engine, 'lokal')
oep_models.Base.metadata.bind = engine

# Add OEP:
engine = sqlalchemy.create_engine(build_db_url('OEP'))
sqlahelper.add_engine(engine, 'oep')
oep_models.Base.metadata.bind = engine

# # Add reiner:
# engine = sqlalchemy.create_engine(build_db_url('reiners_db'))
# sqlahelper.add_engine(engine, 'reiners_db')

LAYERS = ('subst', 'gen', 'rpabw')

LAYER_STYLE = {
    'default': {
        'style': {
            'fillColor': '#888888',
            'weight': 1,
            'opacity': 1,
            'color': 'gray',
            'fillOpacity': 0.25
        }
    },
    'subst': {
        'style': {
            'fillColor': '#ff0000',
            'weight': 1,
            'opacity': 1,
            'color': 'gray',
            'fillOpacity': 0.25
        }
    },
    'gen': {
        'style': {
            'fillColor': '#00aa00',
            'weight': 1,
            'opacity': 1,
            'color': 'gray',
            'fillOpacity': 0.25
        }
    },
    'rpabw': {
        'style': {
            'fillColor': '#444444',
            'weight': 2,
            'opacity': 1,
            'color': 'gray',
            'fillOpacity': 0.25
        }
    }
}
