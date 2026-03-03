from django.core.management.base import BaseCommand
from orders.models import Topping, MenuItem


class Command(BaseCommand):
    help = 'Seed the database with vegan menu items and toppings'

    def handle(self, *args, **options):
        self._seed_toppings()
        self._seed_bowls()
        self._seed_wraps()
        self._seed_salads()
        self._seed_smoothies()
        self._seed_sides()
        self._seed_desserts()
        self.stdout.write(self.style.SUCCESS('Vegan menu seeded successfully!'))

    def _seed_toppings(self):
        toppings = [
            'Avocado', 'Tempeh Bacon', 'Roasted Chickpeas', 'Hemp Seeds',
            'Pickled Onions', 'Jalapeños', 'Crispy Tofu', 'Cashew Crema',
            'Sriracha Drizzle', 'Tahini Dressing', 'Nutritional Yeast',
            'Sun-Dried Tomatoes', 'Kimchi', 'Roasted Sweet Potato',
            'Mango Salsa', 'Pumpkin Seeds', 'Cilantro-Lime Crema',
            'Sauerkraut', 'Coconut Flakes',
        ]
        for name in toppings:
            Topping.objects.get_or_create(name=name)
        self.stdout.write(f'  Created {len(toppings)} toppings')

    def _seed_bowls(self):
        items = [
            ('Buddha Bowl', 'S', '11.95', 2),
            ('Buddha Bowl', 'L', '14.95', 2),
            ('Teriyaki Tempeh Bowl', 'S', '12.50', 2),
            ('Teriyaki Tempeh Bowl', 'L', '15.50', 2),
            ('Mediterranean Bowl', 'S', '11.95', 2),
            ('Mediterranean Bowl', 'L', '14.95', 2),
            ('Spicy Korean Bowl', 'S', '12.95', 3),
            ('Spicy Korean Bowl', 'L', '15.95', 3),
            ('Harvest Bowl', 'S', '11.50', 2),
            ('Harvest Bowl', 'L', '14.50', 2),
            ('Protein Power Bowl', 'S', '13.50', 3),
            ('Protein Power Bowl', 'L', '16.50', 3),
        ]
        for item in items:
            name, size, price = item[0], item[1], item[2]
            toppings = item[3] if len(item) > 3 else 0
            MenuItem.objects.get_or_create(
                name=name, category='bowl', size=size,
                defaults={'price': price, 'toppings_allowed': toppings,
                          'slug': f'bowl-{name.lower().replace(" ", "-")}-{size.lower()}'}
            )
        self.stdout.write(f'  Created {len(items)} bowls')

    def _seed_wraps(self):
        items = [
            ('Falafel Wrap', 'S', '9.95'),
            ('Falafel Wrap', 'L', '12.95'),
            ('BBQ Jackfruit Wrap', 'S', '10.50'),
            ('BBQ Jackfruit Wrap', 'L', '13.50'),
            ('Thai Peanut Wrap', 'S', '9.95'),
            ('Thai Peanut Wrap', 'L', '12.95'),
            ('Caesar Wrap', 'S', '9.50'),
            ('Caesar Wrap', 'L', '12.50'),
            ('Buffalo Cauliflower Wrap', 'S', '10.50'),
            ('Buffalo Cauliflower Wrap', 'L', '13.50'),
            ('Garden Veggie Wrap', 'S', '8.95'),
            ('Garden Veggie Wrap', 'L', '11.95'),
        ]
        for name, size, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='wrap', size=size,
                defaults={'price': price,
                          'slug': f'wrap-{name.lower().replace(" ", "-")}-{size.lower()}'}
            )
        self.stdout.write(f'  Created {len(items)} wraps')

    def _seed_salads(self):
        items = [
            ('Kale Caesar Salad', '10.95'),
            ('Rainbow Quinoa Salad', '11.50'),
            ('Thai Crunch Salad', '10.95'),
            ('Roasted Beet & Walnut Salad', '11.95'),
            ('Garden Greens', '8.50'),
        ]
        for name, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='salad',
                defaults={'price': price,
                          'slug': f'salad-{name.lower().replace(" ", "-").replace("&", "and")}'}
            )
        self.stdout.write(f'  Created {len(items)} salads')

    def _seed_smoothies(self):
        items = [
            ('Green Goddess Smoothie', 'S', '6.95'),
            ('Green Goddess Smoothie', 'L', '8.95'),
            ('Tropical Bliss Smoothie', 'S', '6.95'),
            ('Tropical Bliss Smoothie', 'L', '8.95'),
            ('Berry Antioxidant Smoothie', 'S', '7.50'),
            ('Berry Antioxidant Smoothie', 'L', '9.50'),
            ('Peanut Butter Banana Smoothie', 'S', '7.50'),
            ('Peanut Butter Banana Smoothie', 'L', '9.50'),
            ('Matcha Oat Latte', 'S', '5.95'),
            ('Matcha Oat Latte', 'L', '7.50'),
            ('Golden Turmeric Latte', 'S', '5.50'),
            ('Golden Turmeric Latte', 'L', '7.00'),
        ]
        for name, size, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='smoothie', size=size,
                defaults={'price': price,
                          'slug': f'smoothie-{name.lower().replace(" ", "-")}-{size.lower()}'}
            )
        self.stdout.write(f'  Created {len(items)} smoothies')

    def _seed_sides(self):
        items = [
            ('Sweet Potato Fries', '5.50'),
            ('Crispy Brussels Sprouts', '6.95'),
            ('Avocado Toast', '7.50'),
            ('Garlic Hummus & Pita', '5.95'),
            ('Coconut Cauliflower Bites', '6.50'),
            ('Edamame', '4.95'),
        ]
        for name, price in items:
            MenuItem.objects.get_or_create(
                name=name, category='side',
                defaults={'price': price,
                          'slug': f'side-{name.lower().replace(" ", "-").replace("&", "and")}'}
            )
        self.stdout.write(f'  Created {len(items)} sides')

    def _seed_desserts(self):
        items = [
            ('Açaí Bowl', 'S', '9.50'),
            ('Açaí Bowl', 'L', '12.50'),
            ('Raw Brownie Bites', '6.95'),
            ('Coconut Chia Pudding', '5.95'),
            ('Banana Nice Cream', '6.50'),
            ('Matcha Energy Balls', '4.95'),
        ]
        for item in items:
            if len(item) == 3:
                name, size, price = item
                MenuItem.objects.get_or_create(
                    name=name, category='dessert', size=size,
                    defaults={'price': price,
                              'slug': f'dessert-{name.lower().replace(" ", "-")}-{size.lower()}'}
                )
            else:
                name, price = item[0], item[1]
                MenuItem.objects.get_or_create(
                    name=name, category='dessert',
                    defaults={'price': price,
                              'slug': f'dessert-{name.lower().replace(" ", "-")}'}
                )
        self.stdout.write(f'  Created {len(items)} desserts')
