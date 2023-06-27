from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Buch(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Veröffentlichung')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.uploaded_at = timezone.now()
        return super().save(*args, **kwargs)

