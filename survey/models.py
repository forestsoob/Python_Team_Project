from django.db import models
from django.contrib.auth.models import User
from weather.models import Outfit

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} dislikes {self.outfit.name}"