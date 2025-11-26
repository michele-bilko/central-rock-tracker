"""
project/admin.py
Author: Michele Bilko (mbilko@bu.edu)
CS412 Final Project - Central Rock Gym Route Tracking System
Admin configuration for Django admin interface.
This file configures the Django admin interface for managing gym members,
areas, routes, and completions.
"""

from django.contrib import admin
from .models import Member, Area, Route, Completion


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Member model.
    """
    list_display = ['member_number', 'first_name', 'last_name', 'email', 'is_admin', 'date_joined']
    list_filter = ['is_admin', 'date_joined']
    search_fields = ['first_name', 'last_name', 'email', 'member_number']
    ordering = ['member_number']
    readonly_fields = ['date_joined']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Area model.
    """
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Route model.
    """
    list_display = ['name', 'grade', 'color', 'area', 'setter_name', 'date_set', 'is_active']
    list_filter = ['grade', 'color', 'area', 'is_active', 'date_set']
    search_fields = ['name', 'setter_name', 'area__name']
    ordering = ['-date_set', 'area', 'grade']
    date_hierarchy = 'date_set'
    
    def get_queryset(self, request):
        """
        Optimize queryset to reduce database queries.
        """
        return super().get_queryset(request).select_related('area')


@admin.register(Completion)
class CompletionAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Completion model.
    """
    list_display = ['member', 'route', 'date_completed', 'difficulty_rating']
    list_filter = ['difficulty_rating', 'date_completed', 'route__area', 'route__grade']
    search_fields = ['member__first_name', 'member__last_name', 'route__name', 'notes']
    ordering = ['-date_completed']
    date_hierarchy = 'date_completed'
    
    def get_queryset(self, request):
        """
        Optimize queryset to reduce database queries.
        """
        return super().get_queryset(request).select_related('member', 'route', 'route__area')