from django.contrib import admin
from django.urls import path, include
from .api import MyFilesViewSet


urlpatterns = [
    path('files', MyFilesViewSet.as_view({'post': 'post', 'get': 'list'})),
]
