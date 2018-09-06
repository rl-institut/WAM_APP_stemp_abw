from django.urls import path

from . import views


app_name = 'stemp_abw'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('app/', views.map, name='map')
    ]
