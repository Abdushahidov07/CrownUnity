from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Work)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth')
    search_fields = ('user__username', 'user__email')

@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'sent_time', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('sender__username', 'receiver__username')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration')
    search_fields = ('title', 'description')

@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creation_date', 'replies_count')
    search_fields = ('title', 'content', 'author__username')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'amount', 'donation_date', 'status')
    list_filter = ('status',)
    search_fields = ('donor__username',)

@admin.register(FundingReport)
class FundingReportAdmin(admin.ModelAdmin):
    list_display = ('creation_date', 'amount')
    search_fields = ('expense_description',)
