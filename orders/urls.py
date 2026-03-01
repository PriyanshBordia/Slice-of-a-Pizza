from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu_view, name='menu'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_history, name='order_history'),
]
