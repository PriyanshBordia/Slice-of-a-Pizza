import time

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import admin

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")

    return render(request, "orders/index.html", context={"pinnoconame": request.user})


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

    user = User(first_name=first, last_name=last, username=username,
                email=email, password=password, is_staff=False)
    user.save()


def login_view(request):

    username = request.POST.get("username", False)
    password = request.POST.get("password", False)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

    if User.objects.get(username=username, password=password).count() == 0:
        return render(request, "orders/error.html", context={"message": "Please, register to login!"})

    user = User.objects.get()
    return render(request, "orders/menue.html", context={"user": user})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html")


def add_item(request):
    pass
