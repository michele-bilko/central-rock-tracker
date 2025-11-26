"""
project/views.py
Author: Michele Bilko (mbilko@bu.edu)
CS412 Final Project - Central Rock Gym Route Tracking System
Views for handling web requests and user interactions.
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
from .models import Member, Area, Route, Completion
from .forms import CustomUserCreationForm, RouteForm, RouteStatusForm, CompletionForm, ProfileEditForm


def home_view(request):
    """
    Simple home page view.
    TODO: Add personalized content for logged-in users
    TODO: Add recent activity from user's followed climbers
    """
    context = {
        'total_areas': Area.objects.count(),
        'total_routes': Route.objects.filter(is_active=True).count(),
        'total_members': Member.objects.count(),
        'recent_completions': Completion.objects.select_related('member', 'route').order_by('-date_completed')[:5],
    }
    return render(request, 'project/home.html', context)


def login_view(request):
    """
    Custom login view to handle template path issues.
    """
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
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    """
    User registration view.
    TODO: Add email verification
    TODO: Add social login options
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Central Rock Gym!')
            return redirect('project:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def is_admin(user):
    """Helper function to check if user is admin/staff."""
    return user.is_authenticated and (user.is_staff or hasattr(user, 'member') and user.member.is_admin)


@user_passes_test(is_admin)
def admin_members_view(request):
    """
    Admin view to manage members with delete functionality.
    """
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
    
    return render(request, 'project/admin_members.html', context)


@user_passes_test(is_admin)
def delete_member_view(request, pk):
    """
    Admin view to delete a member account.
    """
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
    
    return render(request, 'project/delete_member_confirm.html', context)


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    """
    Admin dashboard with quick stats and management links.
    TODO: Add more detailed analytics
    TODO: Add member management section
    """
    context = {
        'total_routes': Route.objects.count(),
        'active_routes': Route.objects.filter(is_active=True).count(),
        'archived_routes': Route.objects.filter(is_active=False).count(),
        'recent_completions': Completion.objects.select_related('member', 'route').order_by('-date_completed')[:10],
    }
    return render(request, 'project/admin_dashboard.html', context)


@user_passes_test(is_admin)
@user_passes_test(is_admin)
def add_route_view(request):
    """
    Admin view to add new routes.
    TODO: Add bulk route creation
    TODO: Add route photo upload
    """
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save()
            messages.success(request, f'Route "{route}" added successfully!')
            return redirect('project:admin_dashboard')
    else:
        form = RouteForm()
    
    return render(request, 'project/add_route.html', {'form': form})


@user_passes_test(is_admin)
def manage_routes_view(request):
    """
    Admin view to manage existing routes.
    TODO: Add bulk operations
    TODO: Add route editing capability
    """
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'active':
        routes = Route.objects.filter(is_active=True)
    elif filter_type == 'archived':
        routes = Route.objects.filter(is_active=False)
    else:
        routes = Route.objects.all()
    
    routes = routes.select_related('area').order_by('-date_set')
    
    return render(request, 'project/manage_routes.html', {'routes': routes})


@user_passes_test(is_admin)
def toggle_route_status(request, pk):
    """
    Admin view to toggle route active/archived status.
    TODO: Add reason field for status changes
    TODO: Add confirmation step for archiving
    """
    route = get_object_or_404(Route, pk=pk)
    
    if request.method == 'POST':
        route.is_active = 'is_active' in request.POST
        route.save()
        
        status = "activated" if route.is_active else "archived"
        messages.success(request, f'Route "{route}" has been {status}.')
    
    return redirect('project:manage_routes')


class AreaListView(ListView):
    """
    Display list of all climbing areas.
    TODO: Add area statistics (route count, completion count)
    """
    model = Area
    template_name = 'project/area_list.html'
    context_object_name = 'areas'


class AreaDetailView(DetailView):
    """
    Display detailed view of a specific area with its routes.
    TODO: Add area-specific statistics and analytics
    """
    model = Area
    template_name = 'project/area_detail.html'
    context_object_name = 'area'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area = self.get_object()
        
        # Get active routes in this area with completion counts
        routes = Route.objects.filter(area=area, is_active=True).annotate(
            completion_count=Count('completions')
        ).order_by('-date_set')
        
        context['routes'] = routes
        context['total_completions'] = sum(route.completion_count for route in routes)
        
        return context


class RouteListView(ListView):
    """
    Display list of all routes.
    TODO: Add filtering and search capabilities
    """
    model = Route
    template_name = 'project/route_list.html'
    context_object_name = 'routes'
    
    def get_queryset(self):
        return Route.objects.filter(is_active=True).select_related('area').order_by('-date_set')


class RouteDetailView(DetailView):
    """
    Display detailed view of a specific route with completion form.
    TODO: Add route photos and beta
    TODO: Add difficulty consensus calculation
    """
    model = Route
    template_name = 'project/route_detail.html'
    context_object_name = 'route'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route = self.get_object()
        
        # Get completions for this route
        completions = Completion.objects.filter(route=route).select_related('member').order_by('-date_completed')
        context['completions'] = completions
        
        # Check if current user has completed this route
        if self.request.user.is_authenticated:
            try:
                member = self.request.user.member
                user_completion = completions.filter(member=member).first()
                context['user_has_completed'] = bool(user_completion)
                context['user_completion'] = user_completion
            except:
                context['user_has_completed'] = False
        
        # Add completion form for logged-in users
        if self.request.user.is_authenticated and route.is_active:
            context['form'] = CompletionForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle completion form submission.
        """
        route = self.get_object()
        
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to log completions.')
            return redirect('project:login')
        
        try:
            member = request.user.member
        except:
            messages.error(request, 'Member profile not found.')
            return redirect('project:route_detail', pk=route.pk)
        
        # Check if user already completed this route
        if Completion.objects.filter(member=member, route=route).exists():
            messages.warning(request, 'You have already logged a completion for this route.')
            return redirect('project:route_detail', pk=route.pk)
        
        form = CompletionForm(request.POST)
        if form.is_valid():
            completion = form.save(commit=False)
            completion.member = member
            completion.route = route
            completion.save()
            
            messages.success(request, f'Completion logged for "{route}"! Great job!')
            return redirect('project:route_detail', pk=route.pk)
        
        # If form is invalid, reload page with errors
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


@user_passes_test(is_admin)
def admin_completions_view(request):
    """
    Admin view to see all route completions with filtering options.
    """
    # Get filter parameters
    route_filter = request.GET.get('route')
    member_filter = request.GET.get('member')
    area_filter = request.GET.get('area')
    date_filter = request.GET.get('date_range', '30')  # Default to last 30 days
    
    # Start with all completions
    completions = Completion.objects.select_related('member', 'route', 'route__area').order_by('-date_completed')
    
    # Apply filters
    if route_filter:
        completions = completions.filter(route__id=route_filter)
    
    if member_filter:
        completions = completions.filter(member__id=member_filter)
    
    if area_filter:
        completions = completions.filter(route__area__id=area_filter)
    
    # Date range filter
    if date_filter and date_filter != 'all':
        try:
            days = int(date_filter)
            cutoff_date = timezone.now().date() - timedelta(days=days)
            completions = completions.filter(date_completed__gte=cutoff_date)
        except ValueError:
            pass
    
    # Get filter options for dropdowns
    all_routes = Route.objects.filter(is_active=True).order_by('area__name', 'grade')
    all_members = Member.objects.order_by('first_name', 'last_name')
    all_areas = Area.objects.order_by('name')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(completions, 50)  # Show 50 completions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'completions': page_obj,
        'all_routes': all_routes,
        'all_members': all_members,
        'all_areas': all_areas,
        'current_filters': {
            'route': route_filter,
            'member': member_filter,
            'area': area_filter,
            'date_range': date_filter,
        },
        'total_completions': completions.count(),
    }
    
    return render(request, 'project/admin_completions.html', context)


@login_required
def profile_view(request):
    """
    User profile page showing personal stats and recent completions.
    """
    try:
        member = request.user.member
    except:
        # If no member profile exists, create one
        member = Member.objects.create(
            user=request.user,
            first_name=request.user.first_name or 'Unknown',
            last_name=request.user.last_name or 'User',
            email=request.user.email,
            member_number=request.user.id + 10000  # Simple member number generation
        )
    
    # Get user's completions with related data
    completions = Completion.objects.filter(member=member).select_related('route', 'route__area').order_by('-date_completed')
    
    # Calculate statistics
    total_completions = completions.count()
    unique_routes = completions.values('route').distinct().count()
    
    # Grade distribution
    grade_counts = {}
    for completion in completions:
        grade = completion.route.grade
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    # Recent activity (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_completions = completions.filter(date_completed__gte=thirty_days_ago)
    
    # Areas climbed
    areas_climbed = completions.values('route__area__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'member': member,
        'completions': completions[:10],  # Show recent 10
        'total_completions': total_completions,
        'unique_routes': unique_routes,
        'grade_counts': grade_counts,
        'recent_activity_count': recent_completions.count(),
        'areas_climbed': areas_climbed,
    }
    
    return render(request, 'project/profile.html', context)


@login_required
def edit_profile_view(request):
    """
    Edit user profile information.
    """
    try:
        member = request.user.member
    except:
        member = Member.objects.create(
            user=request.user,
            first_name=request.user.first_name or 'Unknown',
            last_name=request.user.last_name or 'User',
            email=request.user.email,
            member_number=request.user.id + 10000
        )
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=member, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('project:profile')
    else:
        form = ProfileEditForm(instance=member, user=request.user)
    
    return render(request, 'project/edit_profile.html', {'form': form})


class MemberListView(UserPassesTestMixin, ListView):
    """
    Display list of all members - ADMIN ONLY.
    TODO: Add member search and filtering
    TODO: Add member statistics
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
        """Redirect non-admin users with a message."""
        messages.error(self.request, 'You must be an administrator to view the member directory.')
        return redirect('project:home')
    
    def get_queryset(self):
        return Member.objects.order_by('first_name', 'last_name')