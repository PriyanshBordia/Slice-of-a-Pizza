from django.core.management.base import BaseCommand
from orders.models import Topping, MenuItem


class Command(BaseCommand):
    help = 'Seed the database with menu items and toppings'

    def handle(self, *args, **options):
        self._seed_toppings()
        self._seed_regular_pizzas()
        self._seed_sicilian_pizzas()
        self._seed_subs()
        self._seed_salads()
        self._seed_pasta()
        self._seed_dinner_platters()
        self.stdout.write(self.style.SUCCESS('Menu seeded successfully!'))

    def _seed_toppings(self):
        toppings = [
            'Pepperoni', 'Sausage', 'Mushrooms', 'Onions', 'Ham',
            'Canadian Bacon', 'Pineapple', 'Eggplant', 'Tomato & Basil',
            'Green Peppers', 'Hamburger', 'Spinach', 'Artichoke',
            'Buffalo Chicken', 'Barbecue Chicken', 'Anchovies',
            'Black Olives', 'Fresh Garlic', 'Zucchini',
        ]
        for name in toppings:
            Topping.objects.get_or_create(name=name)
        self.stdout.write(f'  Created {len(toppings)} toppings')

    def _seed_regular_pizzas(self):
        items = [
            ('Cheese Pizza', 'S', '12.70'),
            ('Cheese Pizza', 'L', '17.95'),
            ('1 Topping Pizza', 'S', '13.70', 1),
            ('1 Topping Pizza', 'L', '19.95', 1),
            ('2 Topping Pizza', 'S', '15.20', 2),
            ('2 Topping Pizza', 'L', '21.95', 2),
            ('3 Topping Pizza', 'S', '16.20', 3),
            ('3 Topping Pizza', 'L', '23.95', 3),
            ('Special Pizza', 'S', '17.75', 5),
            ('Special Pizza', 'L', '25.95', 5),
        ]
        for item in items:
            name, size, price = item[0], item[1], item[2]
            toppings = item[3] if len(item) > 3 else 0
            MenuItem.objects.get_or_create(
                name=name, category='regular_pizza', size=size,
                defaults={'price': price, 'toppings_allowed': toppings,
                          'slug': f'regular-{name.lower().replace(" ", "-")}-{size.lower()}'}
            )
        self.stdout.write(f'  Created {len(items)} regular pizzas')

    def _seed_sicilian_pizzas(self):
        items = [
            ('Cheese Pizza', 'S', '24.45'),
            ('Cheese Pizza', 'L', '38.70'),
            ('1 Topping Pizza', 'S', '26.45', 1),
            ('1 Topping Pizza', 'L', '40.70', 1),
            ('2 Topping Pizza', 'S', '28.45', 2),
            ('2 Topping Pizza', 'L', '42.70', 2),
            ('3 Topping Pizza', 'S', '29.45', 3),
            ('3 Topping Pizza', 'L', '44.70', 3),
            ('Special Pizza', 'S', '30.45', 5),
            ('Special Pizza', 'L', '46.70', 5),
        ]
        for item in items:
            name, size, price = item[0], item[1], item[2]
            toppings = item[3] if len(item) > 3 else 0
            MenuItem.objects.get_or_create(
                name=name, category='sicilian_pizza', size=size,
                defaults={'price': price, 'toppings_allowed': toppings,
                          'slug': f'sicilian-{name.lower().replace(" ", "-")}-{size.lower()}'}
            )
        self.stdout.write(f'  Created {len(items)} sicilian pizzas')

    def _seed_subs(self):
        items = [
            ('Cheese Sub', 'S', '6.50'),
            ('Cheese Sub', 'L', '7.95'),
            ('Italian Sub', 'S', '6.50'),
            ('Italian Sub', 'L', '7.95'),
            ('Ham + Cheese Sub', 'S', '6.50'),
            ('Ham + Cheese Sub', 'L', '7.95'),
            ('Meatball Sub', 'S', '6.50'),
            ('Meatball Sub', 'L', '7.95'),
            ('Tuna Sub', 'S', '6.50'),
            ('Tuna Sub', 'L', '7.95'),
            ('Turkey Sub', 'S', '7.50'),
            ('Turkey Sub', 'L', '8.50'),
            ('Chicken Parm Sub', 'S', '7.50'),
            ('Chicken Parm Sub', 'L', '8.50'),
            ('Eggplant Parm Sub', 'S', '6.50'),
            ('Eggplant Parm Sub', 'L', '7.95'),
            ('Steak Sub', 'S', '6.50'),
            ('Steak Sub', 'L', '7.95'),
            ('Steak + Cheese Sub', 'S', '6.95'),
            ('Steak + Cheese Sub', 'L', '8.50'),
            ('Steak + Mushrooms Sub', 'S', '6.95'),
            ('Steak + Mushrooms Sub', 'L', '8.50'),
            ('Steak + Peppers Sub', 'S', '6.95'),
            ('Steak + Peppers Sub', 'L', '8.50'),
            ('Steak + Onions Sub', 'S', '6.95'),
            ('Steak + Onions Sub', 'L', '8.50'),
            ('Hamburger Sub', 'S', '4.60'),
            ('Hamburger Sub', 'L', '6.95'),
            ('Cheeseburger Sub', 'S', '5.10'),
            ('Cheeseburger Sub', 'L', '7.45'),
            ('Fried Chicken Sub', 'S', '6.95'),
            ('Fried Chicken Sub', 'L', '8.50'),
            ('Veggie Sub', 'S', '6.95'),
            ('Veggie Sub', 'L', '8.50'),
            ('Sausage + Peppers + Onions Sub', 'S', '8.50'),
            ('Sausage + Peppers + Onions Sub', 'L', '13.50'),
        ]
        for name, size, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='sub', size=size,
                defaults={'price': price,
                          'slug': f'sub-{name.lower().replace(" ", "-").replace("+", "and")}-{size.lower()}'}
            )
        self.stdout.write(f'  Created {len(items)} subs')

    def _seed_salads(self):
        items = [
            ('Garden Salad', '6.25'),
            ('Greek Salad', '8.25'),
            ('Antipasto', '8.25'),
            ('Salad w/ Tuna', '8.25'),
        ]
        for name, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='salad',
                defaults={'price': price,
                          'slug': f'salad-{name.lower().replace(" ", "-").replace("/", "")}'}
            )
        self.stdout.write(f'  Created {len(items)} salads')

    def _seed_pasta(self):
        items = [
            ('Baked Ziti w/ Mozzarella', '6.50'),
            ('Baked Ziti w/ Meatballs', '8.75'),
            ('Baked Ziti w/ Chicken', '9.75'),
        ]
        for name, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='pasta',
                defaults={'price': price,
                          'slug': f'pasta-{name.lower().replace(" ", "-").replace("/", "")}'}
            )
        self.stdout.write(f'  Created {len(items)} pasta items')

    def _seed_dinner_platters(self):
        items = [
            ('Garden Salad Platter', 'S', '35.00'),
            ('Garden Salad Platter', 'L', '60.00'),
            ('Greek Salad Platter', 'S', '45.00'),
            ('Greek Salad Platter', 'L', '70.00'),
            ('Antipasto Platter', 'S', '45.00'),
            ('Antipasto Platter', 'L', '70.00'),
            ('Baked Ziti Platter', 'S', '35.00'),
            ('Baked Ziti Platter', 'L', '60.00'),
            ('Meatball Parm Platter', 'S', '45.00'),
            ('Meatball Parm Platter', 'L', '70.00'),
            ('Chicken Parm Platter', 'S', '45.00'),
            ('Chicken Parm Platter', 'L', '70.00'),
        ]
        for name, size, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='dinner_platter', size=size,
                defaults={'price': price,
                          'slug': f'platter-{name.lower().replace(" ", "-")}-{size.lower()}'}
            )
        self.stdout.write(f'  Created {len(items)} dinner platters')
