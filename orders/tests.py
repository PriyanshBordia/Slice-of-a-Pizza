from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Topping, MenuItem, Cart, CartItem, Order, OrderItem


class ToppingModelTest(TestCase):
    def test_create_topping(self):
        t = Topping.objects.create(name='Avocado', slug='avocado')
        self.assertEqual(str(t), 'Avocado')

    def test_auto_slug(self):
        t = Topping(name='Fresh Garlic')
        t.save()
        self.assertEqual(t.slug, 'fresh-garlic')


class MenuItemModelTest(TestCase):
    def test_create_menu_item(self):
        item = MenuItem.objects.create(
            name='Buddha Bowl', category='bowl',
            size='S', price=Decimal('11.95'), slug='bowl-buddha-s'
        )
        self.assertIn('Buddha Bowl', str(item))
        self.assertIn('11.95', str(item))

    def test_size_display(self):
        item = MenuItem.objects.create(
            name='Test', category='salad', price=Decimal('6.00'), slug='test'
        )
        self.assertEqual(item.get_size_display(), '')


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.cart = Cart.objects.create(user=self.user)
        self.item1 = MenuItem.objects.create(
            name='Buddha Bowl', category='bowl',
            size='S', price=Decimal('11.95'), slug='bowl-buddha-s'
        )
        self.item2 = MenuItem.objects.create(
            name='Garden Greens', category='salad',
            price=Decimal('8.50'), slug='garden-greens'
        )

    def test_empty_cart_total(self):
        self.assertEqual(self.cart.total, 0)
        self.assertEqual(self.cart.item_count, 0)

    def test_cart_with_items(self):
        CartItem.objects.create(cart=self.cart, menu_item=self.item1, quantity=2)
        CartItem.objects.create(cart=self.cart, menu_item=self.item2, quantity=1)
        self.assertEqual(self.cart.total, Decimal('32.40'))
        self.assertEqual(self.cart.item_count, 3)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_order(self):
        order = Order.objects.create(user=self.user, total=Decimal('25.40'))
        self.assertEqual(order.status, 'placed')
        OrderItem.objects.create(
            order=order, item_name='Buddha Bowl (Small)', item_price=Decimal('11.95'), quantity=2
        )
        self.assertEqual(order.items.count(), 1)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_redirects_unauthenticated_to_login(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/login.html')

    def test_index_redirects_authenticated_to_menu(self):
        User.objects.create_user(username='test', password='testpass123')
        self.client.login(username='test', password='testpass123')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('menu'))

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post_success(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        })
        self.assertRedirects(response, reverse('menu'))
        self.assertTrue(User.objects.filter(username='johndoe').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'johndoe',
            'password': 'pass1',
            'confirm_password': 'pass2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='johndoe').exists())

    def test_register_duplicate_username(self):
        User.objects.create_user(username='johndoe', password='pass123')
        response = self.client.post(reverse('register'), {
            'username': 'johndoe',
            'password': 'newpass',
            'confirm_password': 'newpass',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        User.objects.create_user(username='test', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'test',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('menu'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        User.objects.create_user(username='test', password='testpass123')
        self.client.login(username='test', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))


class MenuViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpass123')
        self.client = Client()
        self.client.login(username='test', password='testpass123')
        MenuItem.objects.create(
            name='Buddha Bowl', category='bowl',
            size='S', price=Decimal('11.95'), slug='bowl-buddha-s'
        )

    def test_menu_loads(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddha Bowl')

    def test_menu_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('menu'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('menu')}")


class CartFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpass123')
        self.client = Client()
        self.client.login(username='test', password='testpass123')
        self.item = MenuItem.objects.create(
            name='Buddha Bowl', category='bowl',
            size='S', price=Decimal('11.95'), slug='bowl-buddha-s'
        )
        self.topping = Topping.objects.create(name='Avocado', slug='avocado')
        self.item_with_toppings = MenuItem.objects.create(
            name='Protein Power Bowl', category='bowl',
            size='S', price=Decimal('13.50'), slug='bowl-protein-s',
            toppings_allowed=1
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart_add', args=[self.item.id]))
        self.assertRedirects(response, reverse('menu'))
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_with_toppings(self):
        self.client.post(reverse('cart_add', args=[self.item_with_toppings.id]), {
            'toppings': [self.topping.id],
        })
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.toppings.count(), 1)

    def test_view_cart(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_remove_from_cart(self):
        self.client.post(reverse('cart_add', args=[self.item.id]))
        cart_item = CartItem.objects.first()
        response = self.client.post(reverse('cart_remove', args=[cart_item.id]))
        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(CartItem.objects.count(), 0)

    def test_update_quantity(self):
        self.client.post(reverse('cart_add', args=[self.item.id]))
        cart_item = CartItem.objects.first()
        self.client.post(reverse('cart_update', args=[cart_item.id]), {'quantity': 3})
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)


class CheckoutFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpass123')
        self.client = Client()
        self.client.login(username='test', password='testpass123')
        self.item = MenuItem.objects.create(
            name='Buddha Bowl', category='bowl',
            size='S', price=Decimal('11.95'), slug='bowl-buddha-s'
        )
        # Add item to cart
        self.client.post(reverse('cart_add', args=[self.item.id]))

    def test_checkout_get(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddha Bowl')

    def test_checkout_empty_cart(self):
        CartItem.objects.all().delete()
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('cart'))

    def test_place_order(self):
        response = self.client.post(reverse('checkout'), {'notes': 'Extra avocado'})
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total, Decimal('11.95'))
        self.assertEqual(order.notes, 'Extra avocado')
        self.assertEqual(order.items.count(), 1)
        self.assertRedirects(response, f"/order/{order.id}/?placed=1")
        # Cart should be empty
        self.assertEqual(CartItem.objects.count(), 0)

    def test_order_detail(self):
        self.client.post(reverse('checkout'), {})
        order = Order.objects.first()
        response = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 200)

    def test_order_history(self):
        self.client.post(reverse('checkout'), {})
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
