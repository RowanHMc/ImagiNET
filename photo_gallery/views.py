from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib import messages

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
                "Your account was created succesfully"
            )
            return redirect('home')

        else:
            form = RegistrationForm()
        return render(
            request,
            'registration/register.html',
            {'form':form}
        )
