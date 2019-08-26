INSTALLED_APPS = [
    'leaflet',
    'djgeojson',
]

# Leaflet config: variable "LEAFLET_CONFIG" moved to config/leaflet.py since it
# conflicts with other apps using django-leaflet package.
# The leaflet config is now served via views.MapView() (uses settings override
# feature of django-leaflet)
# Related issue: https://github.com/rl-institut/WAM/issues/74
