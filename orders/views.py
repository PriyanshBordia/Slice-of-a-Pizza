from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import MenuItem, Topping, Cart, CartItem, Order, OrderItem


def index(request):
    if request.user.is_authenticated:
        return redirect('menu')
    return render(request, 'orders/login.html')


def register_view(request):
    if request.method == 'GET':
        return render(request, 'orders/registration.html')

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm_password', '')

    if not username or not password:
        messages.error(request, 'Username and password are required.')
        return render(request, 'orders/registration.html')

    if password != confirm_password:
        messages.error(request, 'Passwords do not match.')
        return render(request, 'orders/registration.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username is already taken.')
        return render(request, 'orders/registration.html')

    user = User.objects.create_user(
        username=username, email=email, password=password,
        first_name=first_name, last_name=last_name
    )
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    messages.success(request, f'Welcome, {user.first_name or user.username}!')
    return redirect('menu')


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('menu')
        return render(request, 'orders/login.html')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect('menu')

    messages.error(request, 'Invalid username or password.')
    return render(request, 'orders/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


@login_required(login_url='login')
def menu_view(request):
    categories = MenuItem.CATEGORY_CHOICES
    menu_data = {}
    for code, label in categories:
        items = MenuItem.objects.filter(category=code)
        if items.exists():
            menu_data[label] = items

    toppings = Topping.objects.all().order_by('name')

    cart_count = 0
    if hasattr(request.user, 'cart'):
        cart_count = request.user.cart.item_count

    return render(request, 'orders/menu.html', {
        'menu_data': menu_data,
        'toppings': toppings,
        'cart_count': cart_count,
    })


@require_POST
@login_required(login_url='login')
def cart_add(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.create(cart=cart, menu_item=menu_item)

    # Handle toppings
    topping_ids = request.POST.getlist('toppings')
    if topping_ids and menu_item.toppings_allowed > 0:
        selected_toppings = Topping.objects.filter(id__in=topping_ids)[:menu_item.toppings_allowed]
        cart_item.toppings.set(selected_toppings)

    messages.success(request, f'Added {menu_item.name} to cart.')
    return redirect('menu')


@require_POST
@login_required(login_url='login')
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    name = cart_item.menu_item.name
    cart_item.delete()
    messages.success(request, f'Removed {name} from cart.')
    return redirect('cart')


@require_POST
@login_required(login_url='login')
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        cart_item.delete()
        messages.success(request, f'Removed {cart_item.menu_item.name} from cart.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')
    return redirect('cart')


@login_required(login_url='login')
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('menu_item').prefetch_related('toppings').all()
    return render(request, 'orders/cart.html', {
        'cart': cart,
        'items': items,
    })


@login_required(login_url='login')
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('menu_item').prefetch_related('toppings').all()

    if not items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'GET':
        return render(request, 'orders/checkout.html', {
            'cart': cart,
            'items': items,
        })

    # POST — place order
    notes = request.POST.get('notes', '').strip()
    order = Order.objects.create(
        user=request.user,
        total=cart.total,
        notes=notes,
    )

    for cart_item in items:
        toppings_str = ', '.join(t.name for t in cart_item.toppings.all())
        OrderItem.objects.create(
            order=order,
            item_name=str(cart_item.menu_item),
            item_price=cart_item.menu_item.price,
            toppings_snapshot=toppings_str,
            quantity=cart_item.quantity,
        )

    # Clear cart
    cart.items.all().delete()

    messages.success(request, f'Order #{order.id} placed successfully!')
    return redirect('order_detail', order_id=order.id)


@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})
