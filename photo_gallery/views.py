from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login
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
        'registration/register.html',
        {'form': form}
    )

# Home page
def home(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'photo_gallery/home.html', {
        'photos': photos
    })
