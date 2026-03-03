from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Topping(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('bowl', 'Bowl'),
        ('wrap', 'Wrap'),
        ('salad', 'Salad'),
        ('smoothie', 'Smoothie'),
        ('side', 'Side'),
        ('dessert', 'Dessert'),
    ]
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('L', 'Large'),
    ]

    name = models.CharField(max_length=128)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    toppings_allowed = models.IntegerField(default=0, help_text="Number of toppings allowed (0 = none)")
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        ordering = ['category', 'name', 'size']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.name}-{self.get_size_display()}") if self.size else slugify(self.name)
            self.slug = base
        super().save(*args, **kwargs)

    def __str__(self):
        size_label = f" ({self.get_size_display()})" if self.size else ""
        return f"{self.name}{size_label} - ${self.price}"


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='placed')
    total = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - ${self.total}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    toppings_snapshot = models.CharField(max_length=500, blank=True, default='')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.item_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"
