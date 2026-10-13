from django.shortcuts import render, redirect
from .forms import RegistrationForm, PhotoUploadForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Photo
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login

# Create your views here.

# Register 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Your account was created successfully"
            )
            return redirect('home')
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
    photo= get_object_or_404(Photo, id=photo_id)

    return render(request, 'photo_detail.html',
                  {'photo':photo}
                )


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


