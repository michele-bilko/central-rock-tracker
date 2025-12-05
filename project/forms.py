"""
project/forms.py
Author: Michele Bilko (mbilko@bu.edu)
Central Rock Gym Route Tracking System
Forms for user input and data validation.
UPDATED: Setter name is now a dropdown of admin users
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member, Route, Completion


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user creation form with additional fields for gym members.
    """
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True) 
    email = forms.EmailField(required=True)
    member_number = forms.IntegerField(required=True, help_text="Your gym membership number")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
    
    def clean_member_number(self):
        """Validate that member number is unique."""
        member_number = self.cleaned_data.get('member_number')
        if Member.objects.filter(member_number=member_number).exists():
            raise forms.ValidationError(
                f"Member number {member_number} is already registered. "
                "Please use your unique membership number or contact the gym if you need assistance."
            )
        return member_number
    
    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already registered. Please use a different email or try logging in."
            )
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Create corresponding Member object
            Member.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                member_number=self.cleaned_data['member_number']
            )
        return user


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing user profile information.
    """
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'member_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'member_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            
        # Add CSS classes
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        member = super().save(commit=False)
        
        if self.user and commit:
            # Update User model fields
            self.user.username = self.cleaned_data['username']
            self.user.email = self.cleaned_data['email']
            self.user.first_name = member.first_name
            self.user.last_name = member.last_name
            self.user.save()
            
            # Update Member model
            member.email = self.cleaned_data['email']
            member.save()
            
        return member


class RouteForm(forms.ModelForm):
    """
    Form for adding new climbing routes.
    Setter name is a dropdown of all admin users.
    """
    setter_name = forms.ChoiceField(
        label="Route Setter",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Route
        fields = ['name', 'grade', 'color', 'area', 'date_set', 'setter_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional route name'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'date_set': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all admin users (staff or members with is_admin=True)
        admin_users = []
        
        # Get staff users
        staff_users = User.objects.filter(is_staff=True).order_by('first_name', 'last_name')
        for user in staff_users:
            if user.first_name and user.last_name:
                name = f"{user.first_name} {user.last_name}"
            else:
                name = user.username
            admin_users.append((name, name))
        
        # Get members marked as admin
        admin_members = Member.objects.filter(is_admin=True).order_by('first_name', 'last_name')
        for member in admin_members:
            name = f"{member.first_name} {member.last_name}"
            # Avoid duplicates if they're already in staff
            if (name, name) not in admin_users:
                admin_users.append((name, name))
        
        # Remove duplicates and sort
        admin_users = sorted(list(set(admin_users)), key=lambda x: x[1])
        
        # Set the choices
        self.fields['setter_name'].choices = [('', '-- Select Setter --')] + admin_users
        
        # Set today's date as default
        if not self.instance.pk:
            from django.utils import timezone
            self.fields['date_set'].initial = timezone.now().date()
        
        # If editing existing route, set the setter_name as initial value
        if self.instance.pk and self.instance.setter_name:
            self.fields['setter_name'].initial = self.instance.setter_name


class RouteStatusForm(forms.ModelForm):
    """
    Form for updating route status (active/archived).
    """
    class Meta:
        model = Route
        fields = ['is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class CompletionForm(forms.ModelForm):
    """
    Form for logging route completions.
    """
    class Meta:
        model = Completion
        fields = ['date_completed', 'difficulty_rating', 'notes']
        widgets = {
            'date_completed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'difficulty_rating': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Share your thoughts about this route...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set today's date as default
        if not self.instance.pk:
            from django.utils import timezone
            self.fields['date_completed'].initial = timezone.now().date()