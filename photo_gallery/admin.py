from django.contrib import admin
from .models import Profile, Tag, Photo, PhotoReaction

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)    

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('tags', 'created_at')
    filter_horizontal = ('tags',)

@admin.register(PhotoReaction)
class PhotoReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'reaction')
    list_filter= ('reaction',)