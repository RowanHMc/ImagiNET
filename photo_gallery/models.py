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

"""Photos """
class Photo(models.model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    image = models.ImageField(upload_to='photos/')

    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_photos'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='photos',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

