from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import HvMvSubst


admin.site.register(HvMvSubst, LeafletGeoAdmin)
