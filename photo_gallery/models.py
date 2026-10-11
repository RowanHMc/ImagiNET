from django.db import models
from django.contrib.auth.models import User


# Create your models here.
"""profile model"""
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profie'
    )
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        blank=True,
        
    )
    def __str__(self):
        return self.user.username

"""Tags for search"""
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
 
    

