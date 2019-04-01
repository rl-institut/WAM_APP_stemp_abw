from collections import namedtuple

from django.urls import path, re_path
from djgeojson.views import GeoJSONLayerView
from django.views.decorators.cache import cache_page
from stemp_abw.app_settings import MAP_DATA_CACHE_TIMEOUT

from . import views
from inspect import getmembers, isclass
from meta.models import Source
from meta.views import AppListView, AssumptionsView
#from stemp_abw.views.serial_views import SplitDataView

app_name = 'stemp_abw'

# regular URLs
urlpatterns = [
    path('', views.IndexView.as_view(),
         name='index'),
    path('app/', views.MapView.as_view(),
         name='map'),
    path('imprint/', views.ImprintView.as_view(),
         name='imprint'),
    path('privacy_policy/', views.PrivacyPolicyView.as_view(),
         name='privacy_policy'),
    path('sources_old/', views.SourcesView.as_view(),
         name='sources_old'),
    # Source views from WAM with highlighting
    path('sources/', AppListView.as_view(app_name='stemp_abw',
                                         model=Source),
         name='sources'),
    path('assumptions/', AssumptionsView.as_view(app_name='stemp_abw'),
         name='assumptions'),
    ]

# search detail views classes and append to URLs
detail_views = {}
for name, obj in getmembers(views.detail_views):
    if isclass(obj):
        if issubclass(obj, views.detail_views.MasterDetailView):
            if obj.model is not None:
                detail_views[obj.model.name] = obj
urlpatterns.extend(
    path('popup/{}/<int:pk>/'.format(name), dview.as_view(),
         name='{}-detail'.format(name))
    for name, dview in detail_views.items()
)

# Test JS template view
# TODO: Generalize like above!
urlpatterns.extend(
    [
        path(
            'popupjs/reg_mun_pop/<int:pk>/',
            views.RegMunPopDetailJsView.as_view(),
            name='reg_mun_pop_popupjs'
        ),
        path(
            'popupjs/reg_mun_energy_re_el_dem_share/<int:pk>/',
            views.RegMunEnergyReElDemShareDetailJsView.as_view(),
            name='reg_mun_energy_re_el_dem_share_popupjs'
        ),
        path(
            'popupjs/reg_mun_gen_energy_re/<int:pk>/',
            views.RegMunGenEnergyReDetailJsView.as_view(),
            name='reg_mun_gen_energy_re_popupjs'
        ),
        path(
            'popupjs/reg_mun_gen_energy_re_per_capita/<int:pk>/',
            views.RegMunGenEnergyRePerCapitaDetailJsView.as_view(),
            name='reg_mun_gen_energy_re_per_capita_popupjs'
        ),
        path(
            'popupjs/reg_mun_gen_energy_re_density/<int:pk>/',
            views.RegMunGenEnergyReDensityDetailJsView.as_view(),
            name='reg_mun_gen_energy_re_density_popupjs'
        ),
        path(
            'popupjs/reg_mun_gen_cap_re/<int:pk>/',
            views.RegMunGenCapReDetailJsView.as_view(),
            name='reg_mun_gen_cap_re_popupjs'
        ),
        path(
            'popupjs/reg_mun_gen_cap_re_density/<int:pk>/',
            views.RegMunGenCapReDensityDetailJsView.as_view(),
            name='reg_mun_gen_cap_re_density_popupjs'
        ),
        path(
            'popupjs/reg_mun_dem_el_energy/<int:pk>/',
            views.RegMunDemElEnergyDetailJsView.as_view(),
            name='reg_mun_dem_el_energy_popupjs'
        ),
        path(
            'popupjs/reg_mun_dem_el_energy_per_capita/<int:pk>/',
            views.RegMunDemElEnergyPerCapitaDetailJsView.as_view(),
            name='reg_mun_dem_el_energy_per_capita_popupjs'
        ),
        path(
            'popupjs/reg_mun_dem_th_energy/<int:pk>/',
            views.RegMunDemThEnergyDetailJsView.as_view(),
            name='reg_mun_dem_th_energy_popupjs'
        ),
        path(
            'popupjs/reg_mun_dem_th_energy_per_capita/<int:pk>/',
            views.RegMunDemThEnergyPerCapitaDetailJsView.as_view(),
            name='reg_mun_dem_th_energy_per_capita_popupjs'
        )
    ]
)

# search JSON data views classes and append to URLs
data_views = {}
single_data_views = {}
detail_views_list = {mem[0]: mem[1]
                     for mem in getmembers(views.serial_views, isclass)
                     if mem[1].__module__ == views.serial_views.__name__}
for name, obj in detail_views_list.items():
    if isclass(obj):
        if obj.model is not None:
            # data detail view
            if issubclass(obj, views.GeoJSONSingleDatasetLayerView):
                single_data_views[obj.model.name] = obj
            # data view
            elif issubclass(obj, GeoJSONLayerView):
                data_views[obj.model.name] = obj
# append data views' URLs
urlpatterns.extend(
    re_path(r'^{}.data/'.format(name),
            cache_page(MAP_DATA_CACHE_TIMEOUT)(sview.as_view()),
            name='{}.data'.format(name))
    for name, sview in data_views.items()
)
# append serial detail views' URLs
urlpatterns.extend(
    path('{}/<int:pk>/'.format(name),
            cache_page(MAP_DATA_CACHE_TIMEOUT)(sview.as_view()),
            name='{}.data-detail'.format(name))
    for name, sview in single_data_views.items()
)
