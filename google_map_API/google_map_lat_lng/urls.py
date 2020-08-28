from django.urls import path
from . import views

urlpatterns = [
    path('google_map_lat_lng', views.google_map_lat_lng, name='google_map_lat_lng'),
    path('google_map_lat_lng/look_up', views.look_up, name='look_up')
]
