from collections import namedtuple

from django.urls import path, re_path
from djgeojson.views import GeoJSONLayerView

from . import views

app_name = 'stemp_abw'

# regular URLs
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('app/', views.MapView.as_view(), name='map'),
    path('sources/', views.SourcesView.as_view(), name='sources')
    ]

# append detail views' URLs
detail_views = {'subst': views.SubstDetailView,
                'gen': views.OsmPowerGenDetailView,
                'rpabw': views.RpAbwBoundDetailView,
                'reg_mun': views.RegMunDetailView,
                'reg_prio_area_res': views.RegPrioAreaResDetailView,
                'reg_water_prot_area': views.RegWaterProtAreaDetailView,
                'reg_bird_prot_area': views.RegBirdProtAreaDetailView,
                'reg_bird_prot_area_b200': views.RegBirdProtAreaB200DetailView,
                'reg_nature_prot_area': views.RegNatureProtAreaDetailView,
                'reg_landsc_prot_area': views.RegLandscProtAreaDetailView,
                'reg_resid_area': views.RegResidAreaDetailView,
                'reg_resid_area_b500': views.RegResidAreaB500DetailView,
                'reg_prio_area_flood_prot': views.RegPrioAreaFloodProtDetailView,
                'reg_prio_area_cult': views.RegPrioAreaCultDetailView,
                'reg_forest': views.RegForestDetailView,
                'reg_ffh_prot_area': views.RegFFHProtAreaDetailView,
                'reg_resid_area_b1000': views.RegResidAreaB1000DetailView,
                'reg_prio_area_wec': views.RegPrioAreaWECDetailView,
                'gen_wec': views.GenWECDetailView,
                'reg_dead_zone_hard': views.RegDeadZoneHardDetailView,
                'reg_dead_zone_soft': views.RegDeadZoneSoftDetailView
                }

urlpatterns.extend(
    path('popup/{}/<int:pk>/'.format(name), dview.as_view(), name='{}-detail'.format(name))
    for name, dview in detail_views.items()
)


# append JSON data views' URLs
data_views = {'subst': views.SubstData,
              'gen': views.OsmPowerGenData,
              'rpabw': views.RpAbwBoundData,
              'reg_mun': views.RegMunData,
              'reg_prio_area_res': views.RegPrioAreaResData,
              'reg_water_prot_area': views.RegWaterProtAreaData,
              'reg_bird_prot_area': views.RegBirdProtAreaData,
              'reg_bird_prot_area_b200': views.RegBirdProtAreaB200Data,
              'reg_nature_prot_area': views.RegNatureProtAreaData,
              'reg_landsc_prot_area': views.RegLandscProtAreaData,
              'reg_resid_area': views.RegResidAreaData,
              'reg_resid_area_b500': views.RegResidAreaB500Data,
              'reg_prio_area_flood_prot': views.RegPrioAreaFloodProtData,
              'reg_prio_area_cult': views.RegPrioAreaCultData,
              'reg_forest': views.RegForestData,
              'reg_ffh_prot_area': views.RegFFHProtAreaData,
              'reg_resid_area_b1000': views.RegResidAreaB1000Data,
              'reg_prio_area_wec': views.RegPrioAreaWECData,
              'gen_wec': views.GenWECData,
              'reg_dead_zone_hard': views.RegDeadZoneHardData,
              'reg_dead_zone_soft': views.RegDeadZoneSoftData
              }

urlpatterns.extend(
    re_path(r'^{}.data/'.format(name), sview.as_view(), name='{}.data'.format(name))
    for name, sview in data_views.items()
)
