from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, UserProfile, HelpRequest, ChatMessage, ForumTopic, Donation, Work, Application

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone')

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'gender', 'address', 'profile_picture')

class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = ['location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please describe your situation...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Your current location'})
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message_text']
        widgets = {
            'message_text': forms.TextInput(attrs={'placeholder': 'Type your message...', 'class': 'form-control'})
        }

class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Topic title'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Share your thoughts...'})
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'fund_allocation']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1', 'step': '1', 'class': 'form-control'}),
            'fund_allocation': forms.Select(choices=[
                ('emergency', 'Emergency Support'),
                ('education', 'Education Programs'),
                ('general', 'General Fund')
            ])
        }

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'description', 'category', 'image', 'video', 'region', 'address']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter work title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter work description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message', 'price', 'duration']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your message'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your price'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration (e.g., 2 weeks)'}),
        }
