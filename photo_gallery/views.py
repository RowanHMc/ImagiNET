from django.shortcuts import render, redirect
from .forms import RegistrationForm, PhotoUploadForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Photo


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

