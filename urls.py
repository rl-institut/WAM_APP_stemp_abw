from inspect import getmembers, isclass

from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from djgeojson.views import GeoJSONLayerView

from meta.models import Source
from meta.views import AppListView, AssumptionsView
from stemp_abw.app_settings import MAP_DATA_CACHE_TIMEOUT
from stemp_abw import views

app_name = 'stemp_abw'

# Regular URLs
urlpatterns = [
    path('contact/', views.ContactView.as_view(),
         name='contact'),
    path('', views.IndexView.as_view(),
         name='index'),
    path('app/', views.MapView.as_view(),
         name='map'),
    path('imprint/', views.ImprintView.as_view(),
         name='imprint'),
    path('privacy_policy/', views.PrivacyPolicyView.as_view(),
         name='privacy_policy'),
    # Source views from WAM with highlighting
    path('sources/', AppListView.as_view(app_name=app_name,
                                         model=Source),
         name='sources'),
    path('assumptions/', AssumptionsView.as_view(app_name=app_name),
         name='assumptions'),
    path('sim_status.data', views.SimulationStatus.as_view(),
         name='sim_status.data'),
    path('result_charts.data', views.ResultChartsData.as_view(),
         name='result_charts.data'),
    ]

# Search detail-view-classes and append to URLs
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
urlpatterns.extend(
    path('popupjs/{}/<int:pk>/'.format(name), dview.as_view(
        template_name='stemp_abw/popups/js_popup.html'),
         name='{}-js'.format(name))
    for name, dview in detail_views.items()
)

# Search JSON data-view classes and append to URLs
data_views = {}
single_data_views = {}
detail_views_list = {mem[0]: mem[1]
                     for mem in getmembers(views.serial_views, isclass)
                     if mem[1].__module__ == views.serial_views.__name__}
for name, obj in detail_views_list.items():
    if isclass(obj):
        if getattr(obj, 'model', None) is not None:
            # serial data detail view
            if issubclass(obj, views.GeoJSONSingleDatasetLayerView):
                single_data_views[obj.model.name] = obj
            # serial data view
            elif issubclass(obj, GeoJSONLayerView):
                data_views[obj.model.name] = obj
        elif getattr(obj, 'model_name', None) is not None:
            # serial data result view
            if issubclass(obj, views.GeoJSONResultLayerData):
                data_views[obj.model_name] = obj
# Append data-views' URLs
urlpatterns.extend(
    re_path(r'^{}.data/'.format(name),
            cache_page(MAP_DATA_CACHE_TIMEOUT)(sview.as_view()),
            name='{}.data'.format(name))
    for name, sview in data_views.items()
)
# Append serial detail-views' URLs
urlpatterns.extend(
    path('{}.data/<int:pk>/'.format(name),
            cache_page(MAP_DATA_CACHE_TIMEOUT)(sview.as_view()),
            name='{}.data'.format(name))
    for name, sview in single_data_views.items()
)
