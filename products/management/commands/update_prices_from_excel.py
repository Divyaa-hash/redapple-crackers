from django.core.management.base import BaseCommand
from products.models import Product, Category
import pandas as pd
import os


class Command(BaseCommand):
    help = 'Update product names and prices from Excel file with 10% markup'

    def handle(self, *args, **options):
        excel_file = 'BABY CRACKERS 2026 (1) (1).xlsx'
        
        if not os.path.exists(excel_file):
            self.stdout.write(self.style.ERROR(f'Excel file not found: {excel_file}'))
            return
        
        # Read Excel file - try to detect structure
        df = pd.read_excel(excel_file, header=None)
        self.stdout.write(f'Loaded {len(df)} rows from Excel file')
        self.stdout.write(f'Shape: {df.shape}')
        
        updated_count = 0
        not_found_count = 0
        created_count = 0
        
        current_category = 'GENERAL'
        
        for index, row in df.iterrows():
            # Skip empty rows
            if pd.isna(row[0]) and pd.isna(row[1]):
                continue
            
            # Check if this is a category row (first column is NaN, second column has text)
            if pd.isna(row[0]) and not pd.isna(row[1]):
                current_category = str(row[1]).strip()
                self.stdout.write(f'Found category: {current_category}')
                continue
            
            # Skip if no product name (column 1)
            if pd.isna(row[1]):
                continue
            
            product_name = str(row[1]).strip()
            unit = str(row[2]).strip() if not pd.isna(row[2]) else '1 Pkt'
            original_price = row[3]
            
            # Skip if price is NaN or invalid
            if pd.isna(original_price) or original_price == '' or original_price == 'nan':
                self.stdout.write(self.style.WARNING(f'Skipped: {product_name} - Invalid price'))
                continue
            
            try:
                original_price = float(original_price)
            except (ValueError, TypeError):
                self.stdout.write(self.style.WARNING(f'Skipped: {product_name} - Invalid price format'))
                continue
            
            # Apply 10% markup
            new_price = original_price * 1.1
            
            # Try to find existing product by name (case-insensitive)
            product = Product.objects.filter(name__icontains=product_name).first()
            
            if product:
                # Update existing product
                old_name = product.name
                old_price = product.regular_price
                
                product.name = product_name
                product.regular_price = new_price
                product.save()
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated: {old_name} -> {product_name} | '
                        f'Price: ₹{old_price} -> ₹{new_price:.2f}'
                    )
                )
            else:
                # Try to find or create category
                category = Category.objects.filter(name__icontains=current_category).first()
                if not category:
                    category = Category.objects.create(
                        name=current_category,
                        slug=current_category.lower().replace(' ', '-'),
                        is_active=True
                    )
                    self.stdout.write(self.style.WARNING(f'Created category: {current_category}'))
                
                # Create new product
                slug = product_name.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace('"', '')
                sku = slug[:50]
                
                # Ensure slug is unique
                base_slug = slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                # Ensure sku is unique
                base_sku = sku
                sku_counter = 1
                while Product.objects.filter(sku=sku).exists():
                    sku = f"{base_sku}-{sku_counter}"
                    sku_counter += 1
                
                product = Product.objects.create(
                    name=product_name,
                    slug=slug,
                    sku=sku,
                    category=category,
                    regular_price=new_price,
                    short_description=f'{product_name} - Premium quality crackers',
                    description=f'{product_name} from {current_category}. Premium quality fireworks for your celebrations.',
                    stock=100,
                    is_active=True,
                    is_new=True
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created: {product_name} | Price: ₹{new_price:.2f} | Category: {current_category}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Updated products: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'Created products: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Not found: {not_found_count}'))
        self.stdout.write(self.style.SUCCESS('Price update completed with 10% markup applied!'))
