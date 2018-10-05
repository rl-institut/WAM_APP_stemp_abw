from django.urls import path, re_path
from djgeojson.views import GeoJSONLayerView

from . import views

app_name = 'stemp_abw'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('app/', views.MapView.as_view(), name='map'),

    # Detail data
    path('popup/subst/<int:pk>/', views.SubstDetailView.as_view(), name='subst-detail'),
    path('popup/gen/<int:pk>/', views.OsmPowerGenDetailView.as_view(), name='gen-detail'),
    path('popup/rpabw/<int:pk>/', views.RpAbwBoundDetailView.as_view(), name='rpabw-detail'),

    # JSON Data
    re_path(r'^subst.data/', views.SubstData.as_view(), name='subst.data'),
    re_path(r'^gen.data/', views.OsmPowerGenData.as_view(), name='gen.data'),
    re_path(r'^rpabw.data/', views.RpAbwBoundData.as_view(), name='rpabw.data'),

    # Old stuff
    path('subst/<int:pk>/', views.HvMvSubstDetailView.as_view(), name='subst-detail'),
    path('subst/', views.HvMvSubstView.as_view(), name='subst')

    ]
