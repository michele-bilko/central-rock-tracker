"""
project/urls.py
Author: Michele Bilko (mbilko@bu.edu)
CS412 Final Project - Central Rock Gym Route Tracking System
URL configurations including authentication and admin features.
"""

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'project'

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # Authentication URLs - Use custom views
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/add-route/', views.add_route_view, name='add_route'),
    path('admin/manage-routes/', views.manage_routes_view, name='manage_routes'),
    path('admin/route/<int:pk>/toggle-status/', views.toggle_route_status, name='toggle_route_status'),
    path('admin/completions/', views.admin_completions_view, name='admin_completions'),
    path('admin/members/', views.admin_members_view, name='admin_members'),
    path('admin/members/<int:pk>/delete/', views.delete_member_view, name='delete_member'),
    
    
    # Area URLs
    path('areas/', views.AreaListView.as_view(), name='area_list'),
    path('areas/<int:pk>/', views.AreaDetailView.as_view(), name='area_detail'),
    
    # Route URLs
    path('routes/', views.RouteListView.as_view(), name='route_list'),
    path('routes/<int:pk>/', views.RouteDetailView.as_view(), name='route_detail'),
    
    # Member URLs
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]

# TODO: Add member detail URLs
# TODO: Add completion list URLs  
# TODO: Add API endpoints for mobile app