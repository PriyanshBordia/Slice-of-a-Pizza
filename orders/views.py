import time

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")

    else:
        return render(request, "orders/index.html", context={"pinnoconame": request.user})


def login_view(request):

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not  None:
        login(request, user)

    if User.objects.get(username=username, password=password).count() == 0:
        return render(request, "orders/error.html", context={"message": "Please, register to login!"})

    else:
        user = User.objects.get()
        return render(request, "orders/menue.html", context={"user": user})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html")

def register_view(request):

    first = request.POST["first"]
    last = request.POST["last"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]

# Check for username if present in records if yes, raise error
        # 1. Already a user
        # 2. username unavailable
    if username in User:
        return render(request, "orders/error.html", context={"message": "Username Already taken!"})

    if password != re_password:
        return render(request, "orders/error.html", context={"message": "Passwords don't match"})

    user = User(first_name=first, last_name=last, username=username, email=email, password=password, is_staff=False)
    user.save()
