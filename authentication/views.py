from django.shortcuts import render, redirect



def register_user(request):
    context = {
        "page_name": "Register User",
    }
    return render(
        request,
        "authentication/register_user.html",
        context,
    )


def login_user(request):
    context = {
        "page_name": "Login User",
    }
    return render(
        request,
        "authentication/login_user.html",
        context,
    )


def logout_user(request):
    return redirect('main')
