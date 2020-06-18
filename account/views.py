from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', dict(section='dashboard'))


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            Profile.objects.create(user=new_user)
            login(request, new_user)
            messages.success(request, 'Account registered successfully')
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()

    ctx = dict(user_form=user_form)
    return render(request, 'account/register.html', ctx)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    ctx = dict(user_form=user_form, profile_form=profile_form)
    return render(request, 'account/edit.html', ctx)
