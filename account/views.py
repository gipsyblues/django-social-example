from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', dict(section='dashboard'))


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()

    ctx = dict(user_form=user_form)
    return render(request, 'account/register.html', ctx)
