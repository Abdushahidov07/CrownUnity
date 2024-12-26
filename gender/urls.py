from django.urls import path
from . import views
from.views import *
from .views import CategoryListView, RegionListView, WorkListView

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
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('regions/', RegionListView.as_view(), name='region_list'),
    path('works/', WorkListView.as_view(), name='work_list'),
    path("work_create/", work_create_view, name="work_create"),
    path("work_detail/<int:pk>/", work_detail_view, name="work_detail"),
    path("application_create/<int:pk>/", application_create_view, name="application_create"),
    path("application_list/", application_list_view, name="application_list"),
    path("application_detail/<int:pk>/", application_detail_view, name="application_detail"),
    path("application_update/<int:pk>/", application_update_view, name="application_update"),
    path("application_delete/<int:pk>/", application_delete_view, name="application_delete"),
    path("work_update/<int:pk>/", work_update_view, name="work_update"),
    path("work_delete/<int:pk>/", work_delete_view, name="work_delete"),
    path('my-applications/', my_applications_view, name='my_applications'),
    path('application/<int:pk>/accept/', accept_application, name='accept_application'),
]
