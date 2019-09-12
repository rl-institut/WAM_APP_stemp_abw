# The settings in this file will be global project settings in wam.settings

from stemp_abw.app_settings import DEFAULT_LANGUAGE


INSTALLED_APPS = [
    'leaflet',
    'djgeojson',
]

# Default project language (for available app languages see LANGUAGE_STORE in
# app_settings.py). If this is not present i18n in stemp_abw app will not work.
# This might overwrite the default language of other apps, if the WAM project
# base is combined with other WAM apps that use a different default language.
LANGUAGE_CODE = DEFAULT_LANGUAGE

# Leaflet config: variable "LEAFLET_CONFIG" moved to config/leaflet.py since it
# conflicts with other apps using django-leaflet package.
# The leaflet config is now served via views.MapView() (uses settings override
# feature of django-leaflet)
# Related issue: https://github.com/rl-institut/WAM/issues/74
