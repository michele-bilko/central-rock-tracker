"""
project/models.py
Author: Michele Bilko (mbilko@bu.edu)
CS412 Final Project - Central Rock Gym Route Tracking System
Basic models for the Central Rock Gym route tracking application.
"""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Member(models.Model):
    """
    Represents a gym member.
    This model can exist independently without foreign keys.
    TODO: Add profile picture field
    TODO: Add member preferences (favorite areas, climbing style, etc.)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to Django User
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    member_number = models.IntegerField(unique=True)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('project:member_detail', kwargs={'pk': self.pk})


class Area(models.Model):
    """
    Represents a climbing area within the gym.
    This model can exist independently without foreign keys.
    TODO: Add area image field
    TODO: Add area capacity/max climbers field
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project:area_detail', kwargs={'pk': self.pk})


class Route(models.Model):
    """
    Represents a climbing route within a specific area.
    Requires a foreign key relationship to Area.
    TODO: Add route image field
    TODO: Add route description/beta field
    TODO: Add route tags (overhang, slab, technical, etc.)
    """
    GRADE_CHOICES = [
        ('VB', 'VB'),
        ('V0', 'V0'),
        ('V1', 'V1'),
        ('V2', 'V2'),
        ('V3', 'V3'),
        ('V4', 'V4'),
        ('V5', 'V5'),
    ]
    
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('black', 'Black'),
    ]
    
    name = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    date_set = models.DateField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='routes')
    setter_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        if self.name:
            return f"{self.name} ({self.grade})"
        return f"{self.color.title()} {self.grade}"
    
    def get_absolute_url(self):
        return reverse('project:route_detail', kwargs={'pk': self.pk})
    
    def completion_count(self):
        """Returns the number of times this route has been completed."""
        return self.completions.count()


class Completion(models.Model):
    """
    Represents a member's completion of a specific route.
    Requires foreign key relationships to both Member and Route.
    TODO: Add number of attempts before completion
    TODO: Add completion photo field
    TODO: Add grade opinion field (easier/harder than posted)
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='completions')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='completions')
    date_completed = models.DateField()
    difficulty_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['member', 'route']  # Prevent duplicate completions
    
    def __str__(self):
        return f"{self.member} - {self.route}"
    
    def get_absolute_url(self):
        return reverse('project:route_detail', kwargs={'pk': self.route.pk})