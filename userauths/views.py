from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *


def register_view(request):
    if request.user.is_authenticated:
        return redirect("store:index")
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST or None)

            if form.is_valid():
                new_user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"hey {username}, your account was created successfully")
                new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
                login(request, new_user)
                return redirect("store:index")
        else:
            print('cannot be registered')

    form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'userauths/sign_up.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "hey your already logged in")
        form = UserRegisterForm(request.POST or None)
        return redirect("store:index")

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with {email} does not exist")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "your logged in.")
            return redirect("store:index")
        else:
            messages.warning(request, "user does not exist, create an account")
    context = {}
    return render(request, 'userauths/sign_in.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "your logged out.")
    return redirect("userauths:sign_in")