from django.urls import path, re_path
from djgeojson.views import GeoJSONLayerView

from . import views

app_name = 'stemp_abw'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('app/', views.MapView.as_view(), name='map'),
    #path('app_new/', views.MapNew.as_view(), name='map_new'),
    path('subst/<int:pk>/', views.HvMvSubstDetailView.as_view(), name='subst-detail'),
    path('subst/', views.HvMvSubstView.as_view(), name='subst'),

    # re_path(r'^subst.data/',
    #     GeoJSONLayerView.as_view(model=HvMvSubst,
    #                              properties=(['popup_content', 'name']),
    #                              srid=4326),
    #     name='subst.data'),

    re_path(r'^subst.data/', views.SubstData.as_view(), name='subst.data'),
    re_path(r'^gen.data/', views.OsmPowerGenData.as_view(), name='gen.data'),
    re_path(r'^rpabw.data/', views.RpAbwBoundData.as_view(), name='rpabw.data')

    ]
