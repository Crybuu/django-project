from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import download_file
from .views import delete_file
from django.conf.urls import handler404
from .views import custom_404_page
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import download_file
from .views import delete_file
from django.conf.urls import handler404
from django.views.defaults import page_not_found
from django.shortcuts import render

urlpatterns = [
    path('hello/', views.say_hello),
    path('buch/<int:buch_id>/', views.buch_nach_id, name='Buch_nach_id'),
    path('', views.home, name='home'),
    path('create/', views.create_buch, name='create_buch'),
    #path('ckeditor/', include('ckeditor.urls')),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('uploads/', views.uploads, name='uploads'),
    path('upload/', views.upload_file, name='upload_file'),
    path('playground/download/<path:file_path>/', download_file, name='download_file'),
    path('accounts/user_profiles/', views.user_profiles, name='user_profiles'),
    path('playground/uploads/delete/<int:file_id>/', delete_file, name='delete_file'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




handler404 = 'playground.urls.custom_404_page'

# if settings.DEBUG:
   # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)