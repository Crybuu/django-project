from django import forms
from .models import Buch
from .models import UploadedFile
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile

class BuchForm(forms.ModelForm):
    pub_date = forms.DateTimeField(initial=timezone.now)

    class Meta:
        model = Buch
        fields = ['title', 'pub_date']

class UploadFileForm(forms.Form):
    file = forms.FileField()

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio',)  # Add other fields if needed
