from django.shortcuts import render, redirect
from .forms import RegistrationForm, PhotoUploadForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Photo, PhotoReaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST

# Create your views here.

# Register 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            # login(request, user)

            messages.success(
                request,
                "Your account was created successfully"
            )
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            form.save_m2m()

            messages.success(
                request,
                "Your account was uploaded"
            )
            return redirect('home')
    else:
        form = PhotoUploadForm()

    return render(
        request,
        'upload.html',
        {'form': form}
    )

# Home page
def home(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'home.html', {
        'photos': photos
    })

@login_required
def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    likes_count = photo.reactions.filter(
        reaction=PhotoReaction.LIKE
    ).count()

    dislikes_count = photo.reactions.filter(
        reaction=PhotoReaction.DISLIKE
    ).count()

    user_reaction = None

    if request.user.is_authenticated:
        user_reaction = photo.reactions.filter(
            user=request.user
        ).values_list('reaction', flat=True).first()

    return render(request, 'photo_detail.html', {
        'photo': photo,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_reaction': user_reaction,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully!')
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully!')
        return redirect('home')

    return redirect('home')

@login_required
@require_POST
def react_to_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    reaction_type = request.POST.get('reaction')

    if reaction_type not in [
        PhotoReaction.LIKE,
        PhotoReaction.DISLIKE,
    ]:
        messages.error(request, 'Invalid reaction.')
        return redirect('photo_detail', photo_id=photo.id)

    reaction, created = PhotoReaction.objects.get_or_create(
        user=request.user,
        photo=photo,
        defaults={'reaction': reaction_type},
    )

    if created:
        messages.success(request, 'Your reaction was added.')
    elif reaction.reaction == reaction_type:
        reaction.delete()
        messages.success(request, 'Your reaction was removed.')
    else:
        reaction.reaction = reaction_type
        reaction.save(update_fields=['reaction'])
        messages.success(request, 'Your reaction was updated.')

    return redirect('photo_detail', photo_id=photo.id)
