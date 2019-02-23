from wam.admin import wam_admin_site
from leaflet.admin import LeafletGeoAdmin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from stemp_abw.models import LayerModel

# search geomodels (LayerModel) and register
app_models = apps.get_app_config('stemp_abw').get_models()
for model in app_models:
    try:
        if issubclass(model, LayerModel):
            wam_admin_site.register(model, LeafletGeoAdmin)
        else:
            wam_admin_site.register(model)
    except AlreadyRegistered:
        pass
