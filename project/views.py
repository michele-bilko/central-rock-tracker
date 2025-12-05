"""
project/views.py
Author: Michele Bilko (mbilko@bu.edu)
Central Rock Gym Route Tracking System
Views for handling web requests and user interactions.
UPDATED: Added archive functionality and bulk operations
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Member, Area, Route, Completion
from .forms import CustomUserCreationForm, RouteForm, RouteStatusForm, CompletionForm, ProfileEditForm


def home_view(request):
    """Simple home page view."""
    context = {
        'total_areas': Area.objects.count(),
        'total_routes': Route.objects.filter(is_active=True).count(),
        'total_members': Member.objects.count(),
        'recent_completions': Completion.objects.select_related('member', 'route').order_by('-date_completed')[:5],
    }
    return render(request, 'project/home.html', context)


def login_view(request):
    """Custom login view to handle template path issues."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('project:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'project/login.html', {'form': form})


def register_view(request):
    """Custom registration view with better error handling."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Welcome to Central Rock Gym, {user.first_name}!')
                return redirect('project:home')
            except Exception as e:
                # Catch any unexpected errors during save
                messages.error(request, 'An error occurred during registration. Please try again or contact support.')
                # Log the error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Registration error: {str(e)}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'project/register.html', {'form': form})


def is_admin(user):
    """Helper function to check if user is admin/staff."""
    return user.is_authenticated and (user.is_staff or hasattr(user, 'member') and user.member.is_admin)


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    """Admin dashboard with statistics."""
    total_routes = Route.objects.count()
    active_routes = Route.objects.filter(is_active=True).count()
    archived_routes = Route.objects.filter(is_active=False).count()
    recent_completions = Completion.objects.select_related('member', 'route').order_by('-date_completed')[:10]
    
    context = {
        'total_routes': total_routes,
        'active_routes': active_routes,
        'archived_routes': archived_routes,
        'recent_completions': recent_completions,
    }
    return render(request, 'project/admin_dashboard.html', context)


@user_passes_test(is_admin)
def admin_members_view(request):
    """Admin view to manage members with delete functionality."""
    search_query = request.GET.get('search', '')
    
    members = Member.objects.select_related('user').order_by('first_name', 'last_name')
    
    if search_query:
        members = members.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(member_number__icontains=search_query)
        )
    
    # Add completion counts for each member
    members = members.annotate(completion_count=Count('completions'))
    
    context = {
        'members': members,
        'search_query': search_query,
        'total_members': Member.objects.count(),
    }
    
    return render(request, 'project/manage_members.html', context)


@user_passes_test(is_admin)
def delete_member_view(request, pk):
    """Admin view to delete a member account."""
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'DELETE':
            member_name = f"{member.first_name} {member.last_name}"
            
            # Delete the associated User account (this will cascade to Member)
            if member.user:
                member.user.delete()
            else:
                member.delete()
                
            messages.success(request, f'Member {member_name} has been successfully deleted.')
            return redirect('project:admin_members')
        else:
            messages.error(request, 'Deletion cancelled. You must type "DELETE" to confirm.')
    
    # Get member statistics for confirmation
    completion_count = member.completions.count()
    
    context = {
        'member': member,
        'completion_count': completion_count,
    }
    
    return render(request, 'project/delete_member.html', context)


@user_passes_test(is_admin)
def add_route_view(request):
    """Admin view to add new routes."""
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save()
            messages.success(request, f'Route "{route}" added successfully!')
            # Redirect back to the area if area_id was provided
            area_id = request.POST.get('area_redirect')
            if area_id:
                return redirect('project:area_detail', pk=area_id)
            return redirect('project:admin_dashboard')
    else:
        form = RouteForm()
        # Pre-select area if provided in URL
        area_id = request.GET.get('area')
        if area_id:
            form.fields['area'].initial = area_id
    
    context = {
        'form': form,
        'area_redirect': request.GET.get('area', '')
    }
    
    return render(request, 'project/add_route.html', context)


@user_passes_test(is_admin)
def manage_routes_view(request):
    """Admin view to manage existing routes with bulk operations."""
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'active':
        routes = Route.objects.filter(is_active=True)
    elif filter_type == 'archived':
        routes = Route.objects.filter(is_active=False)
    else:
        routes = Route.objects.all()
    
    routes = routes.select_related('area').order_by('-date_set')
    
    # Get all areas with active route counts for the "Archive by Area" dropdown
    all_areas = Area.objects.annotate(
        active_count=Count('routes', filter=Q(routes__is_active=True))
    ).filter(active_count__gt=0).order_by('name')
    
    context = {
        'routes': routes,
        'filter_type': filter_type,
        'all_areas': all_areas,
    }
    
    return render(request, 'project/manage_routes.html', context)


@user_passes_test(is_admin)
def toggle_route_status(request, pk):
    """Toggle route active/archived status."""
    route = get_object_or_404(Route, pk=pk)
    
    if request.method == 'POST':
        route.is_active = not route.is_active
        route.save()
        
        status = "activated" if route.is_active else "archived"
        messages.success(request, f'Route "{route}" has been {status}.')
    
    return redirect('project:manage_routes')


@user_passes_test(is_admin)
def archived_routes_view(request):
    """
    NEW: View all archived routes with filtering by area.
    """
    area_filter = request.GET.get('area', '')
    
    archived_routes = Route.objects.filter(is_active=False).select_related('area').order_by('-date_set')
    
    if area_filter:
        archived_routes = archived_routes.filter(area__id=area_filter)
    
    # Get all areas for the filter dropdown
    areas = Area.objects.all().order_by('name')
    
    # Count routes by area
    area_counts = Route.objects.filter(is_active=False).values('area__name').annotate(
        count=Count('id')
    ).order_by('area__name')
    
    context = {
        'archived_routes': archived_routes,
        'areas': areas,
        'selected_area': area_filter,
        'total_archived': archived_routes.count(),
        'area_counts': area_counts,
    }
    
    return render(request, 'project/archived_routes.html', context)


@user_passes_test(is_admin)
def bulk_archive_routes(request):
    """
    NEW: Archive multiple routes at once, typically by area.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        area_id = request.POST.get('area_id')
        route_ids = request.POST.getlist('route_ids')
        
        if action == 'archive_area' and area_id:
            # Archive all active routes in a specific area
            area = get_object_or_404(Area, pk=area_id)
            routes = Route.objects.filter(area=area, is_active=True)
            count = routes.count()
            routes.update(is_active=False)
            messages.success(request, f'Archived {count} route(s) in {area.name}.')
            
        elif action == 'archive_selected' and route_ids:
            # Archive specific selected routes
            routes = Route.objects.filter(pk__in=route_ids, is_active=True)
            count = routes.count()
            routes.update(is_active=False)
            messages.success(request, f'Archived {count} selected route(s).')
            
        elif action == 'restore_selected' and route_ids:
            # Restore specific selected routes
            routes = Route.objects.filter(pk__in=route_ids, is_active=False)
            count = routes.count()
            routes.update(is_active=True)
            messages.success(request, f'Restored {count} selected route(s).')
        
        return redirect(request.META.get('HTTP_REFERER', 'project:admin_dashboard'))
    
    return redirect('project:admin_dashboard')


@user_passes_test(is_admin)
def admin_completions_view(request):
    """Admin view to see all completions with filtering."""
    from django.core.paginator import Paginator
    
    # Get filter parameters
    route_filter = request.GET.get('route', '')
    member_filter = request.GET.get('member', '')
    area_filter = request.GET.get('area', '')
    date_range = request.GET.get('date_range', '30')
    
    # Base queryset
    completions = Completion.objects.select_related('member', 'route', 'route__area').order_by('-date_completed')
    
    # Apply filters
    if route_filter:
        completions = completions.filter(route__id=route_filter)
    
    if member_filter:
        completions = completions.filter(member__id=member_filter)
    
    if area_filter:
        completions = completions.filter(route__area__id=area_filter)
    
    if date_range != 'all':
        days = int(date_range)
        cutoff_date = timezone.now().date() - timedelta(days=days)
        completions = completions.filter(date_completed__gte=cutoff_date)
    
    # Pagination
    paginator = Paginator(completions, 20)
    page_number = request.GET.get('page')
    completions_page = paginator.get_page(page_number)
    
    # Get all options for filters
    all_routes = Route.objects.all().order_by('name')
    all_members = Member.objects.all().order_by('first_name', 'last_name')
    all_areas = Area.objects.all().order_by('name')
    
    context = {
        'completions': completions_page,
        'all_routes': all_routes,
        'all_members': all_members,
        'all_areas': all_areas,
        'current_filters': {
            'route': route_filter,
            'member': member_filter,
            'area': area_filter,
            'date_range': date_range,
        },
        'total_completions': completions.count(),
    }
    
    return render(request, 'project/admin_completions.html', context)


# Class-based views

class AreaListView(ListView):
    """
    Display list of all climbing areas with route counts.
    Areas are displayed in a specific order: The Dugout, The Gray Monster, The Warning Track, The Bullpen
    """
    model = Area
    template_name = 'project/area_list.html'
    context_object_name = 'areas'
    
    def get_queryset(self):
        """Add route count annotation and order areas in specific sequence."""
        from django.db.models import Case, When
        
        # Define the custom order
        area_order = ['The Dugout', 'The Gray Monster', 'The Warning Track', 'The Bullpen']
        
        # Create Case/When for ordering
        ordering = Case(
            *[When(name=name, then=pos) for pos, name in enumerate(area_order)],
            default=len(area_order)
        )
        
        return Area.objects.annotate(
            route_count=Count('routes', filter=Q(routes__is_active=True)),
            custom_order=ordering
        ).order_by('custom_order', 'name')


class AreaDetailView(DetailView):
    """Display detailed view of a specific area with its routes."""
    model = Area
    template_name = 'project/area_detail.html'
    context_object_name = 'area'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only show active routes with completion counts
        context['routes'] = self.object.routes.filter(is_active=True).annotate(
            completion_count=Count('completions')
        ).order_by('-date_set')
        context['total_completions'] = Completion.objects.filter(
            route__area=self.object
        ).count()
        return context


class RouteListView(ListView):
    """Display list of all active routes."""
    model = Route
    template_name = 'project/route_list.html'
    context_object_name = 'routes'
    
    def get_queryset(self):
        """Only show active routes."""
        return Route.objects.filter(is_active=True).select_related('area').order_by('-date_set')


class RouteDetailView(DetailView):
    """Display detailed view of a specific route with completion form."""
    model = Route
    template_name = 'project/route_detail.html'
    context_object_name = 'route'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get recent completions
        context['completions'] = self.object.completions.select_related('member').order_by('-date_completed')[:10]
        
        # Check if current user has completed this route
        if self.request.user.is_authenticated and hasattr(self.request.user, 'member'):
            try:
                context['user_completion'] = Completion.objects.get(
                    member=self.request.user.member,
                    route=self.object
                )
                context['user_has_completed'] = True
            except Completion.DoesNotExist:
                context['user_has_completed'] = False
                context['form'] = CompletionForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle completion form submission."""
        self.object = self.get_object()
        
        if not request.user.is_authenticated or not hasattr(request.user, 'member'):
            messages.error(request, 'You must be logged in to log completions.')
            return redirect('project:login')
        
        form = CompletionForm(request.POST)
        if form.is_valid():
            completion = form.save(commit=False)
            completion.member = request.user.member
            completion.route = self.object
            try:
                completion.save()
                messages.success(request, f'Successfully logged completion of {self.object}!')
                return redirect('project:route_detail', pk=self.object.pk)
            except:
                messages.error(request, 'You have already logged this route.')
        
        return self.get(request, *args, **kwargs)


class MemberListView(UserPassesTestMixin, ListView):
    """
    Display list of all members - ADMIN ONLY.
    """
    model = Member
    template_name = 'project/member_list.html'
    context_object_name = 'members'
    
    def test_func(self):
        """Only allow admin/staff users."""
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or 
            (hasattr(self.request.user, 'member') and self.request.user.member.is_admin)
        )
    
    def handle_no_permission(self):
        """Redirect non-admin users with message."""
        messages.error(self.request, 'You must be an admin to view the member list.')
        return redirect('project:home')


@login_required
def profile_view(request):
    """Display user's profile and climbing statistics."""
    if not hasattr(request.user, 'member'):
        messages.error(request, 'No member profile found.')
        return redirect('project:home')
    
    member = request.user.member
    
    # Get completions
    completions = member.completions.select_related('route', 'route__area').order_by('-date_completed')[:10]
    
    # Calculate statistics
    total_completions = member.completions.count()
    unique_routes = member.completions.values('route').distinct().count()
    
    # Recent activity (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_activity_count = member.completions.filter(date_completed__gte=thirty_days_ago).count()
    
    # Grade distribution
    grade_counts = member.completions.values('route__grade').annotate(
        count=Count('id')
    ).order_by('route__grade')
    grade_counts = {item['route__grade']: item['count'] for item in grade_counts}
    
    # Areas climbed
    areas_climbed = member.completions.values('route__area__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'member': member,
        'completions': completions,
        'total_completions': total_completions,
        'unique_routes': unique_routes,
        'recent_activity_count': recent_activity_count,
        'grade_counts': grade_counts,
        'areas_climbed': areas_climbed,
    }
    
    return render(request, 'project/profile.html', context)


@login_required
def edit_profile_view(request):
    """Allow users to edit their profile."""
    if not hasattr(request.user, 'member'):
        messages.error(request, 'No member profile found.')
        return redirect('project:home')
    
    member = request.user.member
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=member, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('project:profile')
    else:
        form = ProfileEditForm(instance=member, user=request.user)
    
    return render(request, 'project/edit_profile.html', {'form': form})