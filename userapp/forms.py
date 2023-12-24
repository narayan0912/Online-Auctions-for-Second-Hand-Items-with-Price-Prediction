from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import UserProfile

class UserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email',)

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name','primary_location', 'date_of_birth', 'phone_number')

        
