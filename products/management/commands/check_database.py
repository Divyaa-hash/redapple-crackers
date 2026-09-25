from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Check database state'

    def handle(self, *args, **options):
        self.stdout.write(f'Total products: {Product.objects.count()}')
        self.stdout.write(f'Total categories: {Category.objects.count()}')

        # First 10 products by order
        self.stdout.write('\nFirst 10 products by order:')
        for p in Product.objects.all().order_by('order')[:10]:
            self.stdout.write(f'{p.order}: {p.name} - {p.image_url}')

        # First 10 products by ID
        self.stdout.write('\nFirst 10 products by ID:')
        for p in Product.objects.all().order_by('id')[:10]:
            self.stdout.write(f'{p.id}: {p.name} - {p.image_url}')

        # Check for old products
        old_products = Product.objects.filter(name__icontains='V.I.P') | Product.objects.filter(name__icontains='Thala') | Product.objects.filter(name__icontains='Family Pack')
        if old_products.exists():
            self.stdout.write(f'\nOld products found: {old_products.count()}')
            for p in old_products:
                self.stdout.write(f'{p.id}: {p.name}')
        else:
            self.stdout.write('\nNo old products found')
