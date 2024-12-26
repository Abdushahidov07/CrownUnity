from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrator'),
        ('user', 'User'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
    )
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    registration_date = models.DateTimeField(default=timezone.now)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

class HelpRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processed', 'Processed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message_text = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    materials_link = models.URLField()

class ForumTopic(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    replies_count = models.IntegerField(default=0)

class Donation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processed', 'Processed'),
    )
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateTimeField(auto_now_add=True)
    fund_allocation = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class FundingReport(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    expense_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
