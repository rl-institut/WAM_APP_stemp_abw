from django.urls import path, re_path
from djgeojson.views import GeoJSONLayerView

from . import views
from .models import HvMvSubst

app_name = 'stemp_abw'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('app/', views.Map.as_view(), name='map'),
    path('subst/<int:pk>/', views.HvMvSubstDetailView.as_view(), name='subst-detail'),
    path('subst/', views.HvMvSubstView.as_view(), name='subst'),

    re_path(r'^data/',
        GeoJSONLayerView.as_view(model=HvMvSubst,
                                 properties=(['popup_content'])),
        name='data')
    ]
