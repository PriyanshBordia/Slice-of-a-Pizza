from django.contrib import admin

from .models import Topping, MenuItem, Cart, CartItem, Order, OrderItem


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'size', 'price', 'toppings_allowed')
    list_filter = ('category', 'size')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(MenuItem, MenuItemAdmin)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'total', 'updated_at')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
