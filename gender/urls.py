from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('help-request/', views.HelpRequestCreateView.as_view(), name='help_request'),
    path('chat/', views.ChatListView.as_view(), name='chat'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('forum/', views.ForumListView.as_view(), name='forum_list'),
    path('forum/create/', views.ForumCreateView.as_view(), name='forum_create'),
    path('donate/', views.DonationCreateView.as_view(), name='donate'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
