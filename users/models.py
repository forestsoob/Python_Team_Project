from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ootd_photo = models.ImageField(upload_to='ootd_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
