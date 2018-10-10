from django.urls import path, re_path
from djgeojson.views import GeoJSONLayerView

from . import views

app_name = 'stemp_abw'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('app/', views.MapView.as_view(), name='map'),
    path('sources/', views.SourcesView.as_view(), name='sources'),

    # Detail data
    path('popup/subst/<int:pk>/', views.SubstDetailView.as_view(), name='subst-detail'),
    path('popup/gen/<int:pk>/', views.OsmPowerGenDetailView.as_view(), name='gen-detail'),
    path('popup/rpabw/<int:pk>/', views.RpAbwBoundDetailView.as_view(), name='rpabw-detail'),
    path('popup/reg_mun/<int:pk>/', views.RegMunDetailView.as_view(), name='reg_mun-detail'),
    path('popup/reg_prio_area_res/<int:pk>/', views.RegPrioAreaResDetailView.as_view(), name='reg_prio_area_res-detail'),
    path('popup/reg_water_prot_area/<int:pk>/', views.RegWaterProtAreaDetailView.as_view(), name='reg_water_prot_area-detail'),
    path('popup/reg_bird_prot_area/<int:pk>/', views.RegBirdProtAreaDetailView.as_view(), name='reg_bird_prot_area-detail'),
    path('popup/reg_bird_prot_area_b200/<int:pk>/', views.RegBirdProtAreaB200DetailView.as_view(), name='reg_bird_prot_area_b200-detail'),
    path('popup/reg_nature_prot_area/<int:pk>/', views.RegNatureProtAreaDetailView.as_view(), name='reg_nature_prot_area-detail'),
    path('popup/reg_landsc_prot_area/<int:pk>/', views.RegLandscProtAreaDetailView.as_view(), name='reg_landsc_prot_area-detail'),
    path('popup/reg_resid_area/<int:pk>/', views.RegResidAreaDetailView.as_view(), name='reg_resid_area-detail'),
    path('popup/reg_resid_area_b500/<int:pk>/', views.RegResidAreaB500DetailView.as_view(), name='reg_resid_area_b500-detail'),
    path('popup/reg_prio_area_flood_prot/<int:pk>/', views.RegPrioAreaFloodProtDetailView.as_view(), name='reg_prio_area_flood_prot-detail'),
    path('popup/reg_prio_area_cult/<int:pk>/', views.RegPrioAreaCultDetailView.as_view(), name='reg_prio_area_cult-detail'),
    path('popup/reg_forest/<int:pk>/', views.RegForestDetailView.as_view(), name='reg_forest-detail'),
    path('popup/reg_ffh_prot_area/<int:pk>/', views.RegFFHProtAreaDetailView.as_view(), name='reg_ffh_prot_area-detail'),
    path('popup/reg_resid_area_b1000/<int:pk>/', views.RegResidAreaB1000DetailView.as_view(), name='reg_resid_area_b1000-detail'),
    path('popup/reg_prio_area_wec/<int:pk>/', views.RegPrioAreaWECDetailView.as_view(), name='reg_prio_area_wec-detail'),
    path('popup/gen_wec/<int:pk>/', views.GenWECDetailView.as_view(), name='gen_wec-detail'),
    path('popup/reg_dead_zone_hard/<int:pk>/', views.RegDeadZoneHardDetailView.as_view(), name='reg_dead_zone_hard-detail'),
    path('popup/reg_dead_zone_soft/<int:pk>/', views.RegDeadZoneSoftDetailView.as_view(), name='reg_dead_zone_soft-detail'),

    # JSON Data
    re_path(r'^subst.data/', views.SubstData.as_view(), name='subst.data'),
    re_path(r'^gen.data/', views.OsmPowerGenData.as_view(), name='gen.data'),
    re_path(r'^rpabw.data/', views.RpAbwBoundData.as_view(), name='rpabw.data'),
    re_path(r'^reg_mun.data/', views.RegMunData.as_view(), name='reg_mun.data'),
    re_path(r'^reg_prio_area_res.data/', views.RegPrioAreaResData.as_view(), name='reg_prio_area_res.data'),
    re_path(r'^reg_water_prot_area.data/', views.RegWaterProtAreaData.as_view(), name='reg_water_prot_area.data'),
    re_path(r'^reg_bird_prot_area.data/', views.RegBirdProtAreaData.as_view(), name='reg_bird_prot_area.data'),
    re_path(r'^reg_bird_prot_area_b200.data/', views.RegBirdProtAreaB200Data.as_view(), name='reg_bird_prot_area_b200.data'),
    re_path(r'^reg_nature_prot_area.data/', views.RegNatureProtAreaData.as_view(), name='reg_nature_prot_area.data'),
    re_path(r'^reg_landsc_prot_area.data/', views.RegLandscProtAreaData.as_view(), name='reg_landsc_prot_area.data'),
    re_path(r'^reg_resid_area.data/', views.RegResidAreaData.as_view(), name='reg_resid_area.data'),
    re_path(r'^reg_resid_area_b500.data/', views.RegResidAreaB500Data.as_view(), name='reg_resid_area_b500.data'),
    re_path(r'^reg_prio_area_flood_prot.data/', views.RegPrioAreaFloodProtData.as_view(), name='reg_prio_area_flood_prot.data'),
    re_path(r'^reg_prio_area_cult.data/', views.RegPrioAreaCultData.as_view(), name='reg_prio_area_cult.data'),
    re_path(r'^reg_forest.data/', views.RegForestData.as_view(), name='reg_forest.data'),
    re_path(r'^reg_ffh_prot_area.data/', views.RegFFHProtAreaData.as_view(), name='reg_ffh_prot_area.data'),
    re_path(r'^reg_resid_area_b1000.data/', views.RegResidAreaB1000Data.as_view(), name='reg_resid_area_b1000.data'),
    re_path(r'^reg_prio_area_wec.data/', views.RegPrioAreaWECData.as_view(), name='reg_prio_area_wec.data'),
    re_path(r'^gen_wec.data/', views.GenWECData.as_view(), name='gen_wec.data'),
    re_path(r'^reg_dead_zone_hard.data/', views.RegDeadZoneHardData.as_view(), name='reg_dead_zone_hard.data'),
    re_path(r'^reg_dead_zone_soft.data/', views.RegDeadZoneSoftData.as_view(), name='reg_dead_zone_soft.data'),

    ]
