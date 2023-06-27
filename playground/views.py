from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .forms import BuchForm
from .models import Buch
from django.conf import settings
import os
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.http import FileResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from mimetypes import guess_type
from .forms import FileUploadForm
from .models import UploadedFile
from .forms import UserProfileForm
from django.http import FileResponse
import mimetypes
from django.template.loader import get_template
from .models import UserProfile
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

def say_hello(request):
    return render(request, 'hello.html', {'name': 'Blerian'})

def buch_nach_id(request, buch_id):
    buch = Buch.objects.get(pk=buch_id)
    return render(request, 'bookdetails.html', {'buch': buch})

def home(request):
    books = Buch.objects.all()
    return render(request, 'index.html', {'books': books})

def create_buch(request):
    if request.method == 'POST':
        form = BuchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BuchForm()

    return render(request, 'createbook.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            profile_form = UserProfileForm(request.POST)
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user  # Associate the profile with the user
                profile.save()  # Save the profile
            return redirect('home')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})

class CustomLoginView(LoginView):
    template_name = 'login.html'


@login_required
def profile(request):
    user_profile = request.user.userprofile
    form = UserProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }

    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def uploads(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'uploads.html', {'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # Construct the absolute file path
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
            # Create the directory path if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Create an UploadedFile instance and associate it with the current user
            uploaded_file_obj = UploadedFile.objects.create(user=request.user, file=file_path)
            uploaded_file_obj.save()
            return redirect('uploads')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


def download_file(request, file_path):
    absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(absolute_path):
        with open(absolute_path, 'rb') as file:
            response = HttpResponse(content_type=guess_type(absolute_path)[0])
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(absolute_path))
            response.write(file.read())
            return response
    else:
        return HttpResponseNotFound("File not found")

@login_required
def user_profiles(request):
    users = User.objects.all()
    return render(request, 'user_profiles.html', {'users': users})

@login_required
def profile_view(request):
    return render(request, 'playground/profile.html')


def delete_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    uploaded_file.file.delete()  # Delete the file from the storage
    uploaded_file.delete()  # Delete the UploadedFile instance from the database
    return redirect('uploads')


def custom_404_page(request, exception):
    return render(request, '404.html', status=404)

