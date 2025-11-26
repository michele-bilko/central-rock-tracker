"""
URL configuration for Central Rock Gym Route Tracking System.
Author: Michele Bilko
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('project.urls')),
]
