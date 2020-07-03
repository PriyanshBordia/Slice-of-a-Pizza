from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    # path("cart", views.cart_view, name="cart"),
    # path("", views., name=""),
    # path("", views., name=""),
]
