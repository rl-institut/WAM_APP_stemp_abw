from wam.admin import wam_admin_site
from leaflet.admin import LeafletGeoAdmin

from .models import HvMvSubst


wam_admin_site.register(HvMvSubst, LeafletGeoAdmin)
