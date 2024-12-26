from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import User, HelpRequest, ChatMessage, Course, ForumTopic, Donation, UserProfile
from .forms import (
    CustomUserCreationForm, CustomPasswordChangeForm, UserProfileForm,
    HelpRequestForm, ChatMessageForm, ForumTopicForm, DonationForm
)

class LandingView(TemplateView):
    template_name = 'gender/landing.html'

class CustomLoginView(LoginView):
    template_name = 'gender/login.html'
    success_url = reverse_lazy('home')
    
    def get_success_url(self):
        return self.success_url

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('landing')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'gender/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'gender/password_change.html'
    success_url = reverse_lazy('home')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'gender/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_requests'] = HelpRequest.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        context['forum_topics'] = ForumTopic.objects.order_by('-creation_date')[:5]
        return context

class HelpRequestCreateView(LoginRequiredMixin, CreateView):
    model = HelpRequest
    form_class = HelpRequestForm
    template_name = 'gender/help_request.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'pending'
        response = super().form_valid(form)
        messages.success(self.request, 'Help request submitted successfully. We will contact you soon.')
        return response

class ChatListView(LoginRequiredMixin, ListView):
    model = ChatMessage
    template_name = 'gender/chat.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return ChatMessage.objects.filter(
            sender=self.request.user
        ).order_by('-sent_time')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            message = request.POST.get('message')
            if message:
                ChatMessage.objects.create(
                    sender=request.user,
                    message_text=message,
                    sent_time=timezone.now()
                )
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'gender/courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all().order_by('title')

class ForumListView(LoginRequiredMixin, ListView):
    model = ForumTopic
    template_name = 'gender/forum_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return ForumTopic.objects.all().order_by('-creation_date')

class ForumCreateView(LoginRequiredMixin, CreateView):
    model = ForumTopic
    form_class = ForumTopicForm
    template_name = 'gender/forum_create.html'
    success_url = reverse_lazy('forum_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Topic created successfully!')
        return response

class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'gender/donate.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.donor = self.request.user
        form.instance.status = 'pending'
        response = super().form_valid(form)
        messages.success(self.request, 'Thank you for your donation! We will process it shortly.')
        return response

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'gender/profile.html'
    success_url = reverse_lazy('profile')
    fields = ['username', 'first_name', 'last_name', 'phone']  # Required fields for UpdateView
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Initialize forms with current data
        context['user_form'] = CustomUserCreationForm(instance=user, initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
        })
        context['profile_form'] = UserProfileForm(instance=profile)
            
        # Add statistics
        context['help_requests_count'] = HelpRequest.objects.filter(user=user).count()
        context['donations_count'] = Donation.objects.filter(donor=user).count()
        
        # Add recent activities
        recent_activities = []
        
        # Add help requests
        help_requests = HelpRequest.objects.filter(user=user).order_by('-created_at')[:5]
        for hr in help_requests:
            recent_activities.append({
                'type': 'help_request',
                'title': 'Help Request',
                'description': hr.description[:100] + '...' if len(hr.description) > 100 else hr.description,
                'date': hr.created_at
            })
        
        # Add donations
        donations = Donation.objects.filter(donor=user).order_by('-donation_date')[:5]
        for donation in donations:
            recent_activities.append({
                'type': 'donation',
                'title': 'Made a Donation',
                'description': f'Donated ${donation.amount} to {donation.fund_allocation}',
                'date': donation.donation_date
            })
        
        # Add forum topics
        forum_topics = ForumTopic.objects.filter(author=user).order_by('-creation_date')[:5]
        for topic in forum_topics:
            recent_activities.append({
                'type': 'forum',
                'title': 'Created Forum Topic',
                'description': topic.title,
                'date': topic.creation_date
            })
        
        # Sort all activities by date
        recent_activities.sort(key=lambda x: x['date'], reverse=True)
        context['recent_activities'] = recent_activities[:10]
        
        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        profile_form = UserProfileForm(self.request.POST, self.request.FILES, instance=user.userprofile)
        
        if profile_form.is_valid():
            user.save()
            profile_form.save()
            messages.success(self.request, 'Profile updated successfully!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
