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
    CHAT_TYPES = [
        ('legal', 'Правовая поддержка'),
        ('psychological', 'Психологическая поддержка'),
        ('general', 'Общая поддержка'),
    ]
    
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    message_text = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_ai_response = models.BooleanField(default=False)
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPES, default='general')

    class Meta:
        ordering = ['sent_time']
        
    def __str__(self):
        return f"{self.sender}: {self.message_text[:50]}"

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


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="static/images/category", null=True, blank=True)
    
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="static/images/region", null=True, blank=True)
    
    def __str__(self):
        return self.name

class Work(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="static/images/work", null=True, blank=True)
    video = models.FileField(upload_to="static/videos/work", max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class Application(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    price = models.IntegerField()
    duration = models.CharField(max_length=50)
    STATUS = (
        ("HIRED", "hired"),
        ("REJECTED", "rejected"),
        ("IN PROCESS", "in process")
    )
    status = models.CharField(choices=STATUS, max_length=50)
    created_on = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('info', 'Информация'),
        ('success', 'Успех'),
        ('warning', 'Предупреждение'),
        ('error', 'Ошибка'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"
