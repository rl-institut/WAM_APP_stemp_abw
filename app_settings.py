import os

from django.utils import translation
from django.utils.translation import gettext_lazy as _
from configobj import ConfigObj

from wam import settings

# TODO: Explain vars!

# Set default language for app
DEFAULT_LANGUAGE = 'de'

# Store which defines all available languages for an app
LANGUAGE_STORE = ['de', 'en']


# Get the language of current app thread or fallback to default language.
def get_language_or_fallback():
    current_thread_language = translation.get_language()
    if current_thread_language in LANGUAGE_STORE:
        return current_thread_language
    else:
        return DEFAULT_LANGUAGE


def layer_areas_metadata():
    language = get_language_or_fallback()
    return ConfigObj(os.path.join(settings.BASE_DIR,
                                    'stemp_abw',
                                    'locale',
                                    language,
                                    'layers_areas.cfg'))


def layer_region_metadata():
    language = get_language_or_fallback()
    return ConfigObj(os.path.join(settings.BASE_DIR,
                                    'stemp_abw',
                                    'locale',
                                    language,
                                    'layers_region.cfg'))


def layer_result_metadata():
    language = get_language_or_fallback()
    return ConfigObj(os.path.join(settings.BASE_DIR,
                                    'stemp_abw',
                                    'locale',
                                    language,
                                    'layers_results.cfg'))


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


def labels():
    language = get_language_or_fallback()
    return ConfigObj(os.path.join(settings.BASE_DIR,
                                    'stemp_abw',
                                    'locale',
                                    language,
                                    'labels.cfg'))


def text_files_dir():
    language = get_language_or_fallback()
    return os.path.join(settings.BASE_DIR,
                                  'stemp_abw',
                                  'locale',
                                  language,
                                  'reveals')


def text_files():
    return {name: {'file': os.path.join(text_files_dir(), f'{name}.md'),
                     'icon': icon}
              for name, icon in
              {'welcome': 'ion-help-buoy',
               'outlook': 'ion-navigate'}.items()
              }


MAP_DATA_CACHE_TIMEOUT = 60 * 60

# Mapping between UI control id and data in scenario data dict.
# The value can be string or list of strings. If a list is provided, the
# control value is calculated using the sum of scenario's data values
CONTROL_VALUES_MAP = {'sl_wind': 'gen_capacity_wind',
                      'sl_pv_roof':
                          ['gen_capacity_pv_roof_large',
                           'gen_capacity_pv_roof_small'],
                      'sl_pv_ground': 'gen_capacity_pv_ground',
                      'sl_bio':
                          ['gen_capacity_bio',
                           'gen_capacity_sewage_landfill_gas'],
                      'sl_conventional':
                          ['gen_capacity_conventional_large',
                           'gen_capacity_conventional_small'],
                      'sl_resid_dem_el': 'resid_dem_el',
                      'sl_crt_dem_el': 'crt_dem_el',
                      'sl_ind_dem_el': 'ind_dem_el',
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


def node_labels():
    return {'gen_el_wind': str(_('Windenergie')),
            'gen_el_pv_roof': str(_('PV Dach')),
            'gen_el_pv_ground': str(_('PV Freifläche')),
            'gen_el_hydro': str(_('Wasserkraft')),
            'gen_el_bio': str(_('Bioenergie')),
            'gen_el_conventional': str(_('Fossil')),
            'dem_el_hh': str(_('Haushalte')),
            'dem_el_rca': str(_('GHD')),
            'dem_el_ind': str(_('Industrie')),
            'shortage_el': str(_('Import')),
            'excess_el': str(_('Export'))
            }


RE_POT_LAYER_ID_LIST = [str(_) for _ in range(1, 7)]

SIMULATION_CFG = {'date_from': '2017-01-01 00:00:00',
                  'date_to': '2017-12-31 23:00:00',
                  'freq': '60min',
                  'solver': 'cbc',
                  'verbose': True,
                  'keepfiles': False
                  }


def month_labels():
    return [
        str(_('Jan')),
        str(_('Feb')),
        str(_('Mär')),
        str(_('Apr')),
        str(_('Mai')),
        str(_('Jun')),
        str(_('Jul')),
        str(_('Aug')),
        str(_('Sep')),
        str(_('Okt')),
        str(_('Nov')),
        str(_('Dez')),
    ]
