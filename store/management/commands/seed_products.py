from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seed database with sample gym products'

    def handle(self, *args, **kwargs):
        # Categories
        cats = {}
        for name in ['Barbells & Plates', 'Dumbbells', 'Cardio', 'Apparel', 'Accessories', 'Recovery']:
            cat, _ = Category.objects.get_or_create(name=name)
            cats[name] = cat

        products = [
            {'name': 'Olympic Barbell 20kg', 'category': 'Barbells & Plates', 'price': '129.99', 'stock': 15, 'description': 'Professional-grade 20kg Olympic barbell. Knurled grip, 28mm diameter, 220,000 PSI tensile strength. Built to last a lifetime.'},
            {'name': 'Bumper Plate Set 100kg', 'category': 'Barbells & Plates', 'price': '249.99', 'stock': 8, 'description': 'High-density rubber bumper plates. Colour-coded by weight. Drop-safe and silent on platforms.'},
            {'name': 'Cast Iron Dumbbell Set', 'category': 'Dumbbells', 'price': '189.99', 'stock': 20, 'description': 'Hex rubber-coated dumbbells. Available 5–30kg pairs. Non-roll design keeps them where you drop them.'},
            {'name': 'Adjustable Dumbbell 32kg', 'category': 'Dumbbells', 'price': '299.99', 'stock': 10, 'description': 'Single adjustable dumbbell replaces 16 pairs. Fast dial-change system. Compact and space-saving.'},
            {'name': 'Air Assault Bike', 'category': 'Cardio', 'price': '799.99', 'stock': 5, 'description': 'Fan bike delivering unlimited resistance. Full-body conditioning in minutes. Used by elite military and CrossFit athletes.'},
            {'name': 'Concept2 Rowing Machine', 'category': 'Cardio', 'price': '1099.99', 'stock': 4, 'description': 'The gold standard in rowing machines. PM5 monitor, foldable for storage. World records are set on this machine.'},
            {'name': 'IronForge Training Tee', 'category': 'Apparel', 'price': '34.99', 'stock': 50, 'description': 'Moisture-wicking, four-way stretch training tee. Flatlock seams for zero chafing. Train hard, look sharp.'},
            {'name': 'Powerlifting Belt 10mm', 'category': 'Accessories', 'price': '89.99', 'stock': 25, 'description': 'Single-prong lever belt, 10mm thick genuine leather. Maximum intra-abdominal pressure for maximum lifts.'},
            {'name': 'Foam Roller PRO', 'category': 'Recovery', 'price': '44.99', 'stock': 30, 'description': 'High-density EVA foam roller with textured surface. Target trigger points, increase mobility, recover faster.'},
            {'name': 'Resistance Band Set', 'category': 'Accessories', 'price': '29.99', 'stock': 40, 'description': 'Set of 5 progressive resistance bands. 5–175 lbs resistance. Perfect for warm-ups, rehab, and bodyweight training.'},
        ]

        for p in products:
            Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': cats[p['category']],
                    'price': p['price'],
                    'stock': p['stock'],
                    'description': p['description'],
                    'is_active': True,
                }
            )
            self.stdout.write(self.style.SUCCESS(f"  ✓ {p['name']}"))

        self.stdout.write(self.style.SUCCESS('\nDone! Sample products added.'))
