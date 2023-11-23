from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import NewUserForm


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("chat:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    context = {
        "register_form": form,
        "page_name": "Register User",
    }
    return render(
        request,
        "authentication/register_user.html",
        context,
    )


def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
	
    
    form = AuthenticationForm()
    context = {
        'login_form': form,
        "page_name": "Login User",
    }
    return render(
        request,
        "authentication/login_user.html",
        context,
    )


@login_required(login_url='authentication:login_user')
def logout_user(request):
    logout(request)
    return redirect("main")
