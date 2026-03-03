def cart_count(request):
    count = 0
    if request.user.is_authenticated and hasattr(request.user, 'cart'):
        count = request.user.cart.item_count
    return {'cart_count': count}
