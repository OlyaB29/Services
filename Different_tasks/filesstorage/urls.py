from django.contrib import admin
from django.urls import path, include
from .api import MyFilesViewSet, SelectelFilesViewSet


urlpatterns = [
    path('files', MyFilesViewSet.as_view({'post': 'post', 'get': 'list'})),
    path('selectel_files', SelectelFilesViewSet.as_view({'post': 'post', 'get': 'list'})),
]
