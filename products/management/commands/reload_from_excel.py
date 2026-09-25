import pandas as pd
import sys
import io
import re
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Reload all products from Excel file in correct order with correct categories and prices'

    def handle(self, *args, **options):
        # Set UTF-8 encoding for stdout
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

        # Read the Excel file
        df = pd.read_excel('Final_Price_List_RAC_2026.xlsx', header=3)

        # Filter out category header rows and empty rows
        df = df[df['Category'].notna()]
        df = df[df['Name of Product (English)'].notna()]

        self.stdout.write(f"Total products in Excel: {len(df)}")

        # Create or update categories
        category_mapping = self.create_or_update_categories(df)

        # Clear existing products
        Product.objects.all().delete()
        self.stdout.write("Cleared all existing products")

        # Add products from Excel
        added_count = 0
        error_count = 0

        for idx, row in df.iterrows():
            try:
                product_name = row['Name of Product (English)'].strip()
                category_name = row['Category'].strip()
                price = float(row['Net Rate (₹)'])
                unit = row['Per / Unit'].strip() if pd.notna(row['Per / Unit']) else '1 Box'

                # Get category
                category = category_mapping.get(category_name)
                if not category:
                    error_count += 1
                    self.stdout.write(f"Error: Category not found: {category_name}")
                    continue

                # Generate unique slug
                slug = product_name.lower()
                slug = re.sub(r'[^a-z0-9\s-]', '', slug)
                slug = re.sub(r'[-\s]+', '-', slug)
                slug = slug[:200]

                # Make slug unique
                base_slug = slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                # Generate unique SKU
                sku = product_name[:45]
                base_sku = sku
                sku_counter = 1
                while Product.objects.filter(sku=sku).exists():
                    sku = f"{base_sku[:45]}-{sku_counter}"
                    sku_counter += 1

                # Create product
                product = Product.objects.create(
                    name=product_name,
                    category=category,
                    sku=sku,
                    regular_price=Decimal(str(price / 0.2)),  # MRP for 80% discount
                    sale_price=Decimal(str(price)),  # Excel price is selling price
                    short_description=f"{product_name} - {unit}",
                    description=f"{product_name} from {category_name}. {unit} pack.",
                    pieces=1,
                    stock=100,
                    is_active=True,
                    image_url='images/crackers/logo.jpg',  # Will be updated by assign_product_images
                    slug=slug,
                    order=idx  # Maintain Excel order
                )

                added_count += 1
                self.stdout.write(f"Added {idx + 1}: {product_name} - {price}")

            except Exception as e:
                error_count += 1
                self.stdout.write(f"Error adding product: {e}")

        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"Added: {added_count} products")
        self.stdout.write(f"Errors: {error_count} products")

    def create_or_update_categories(self, df):
        """Create or update categories from Excel file"""
        category_mapping = {}

        # Get unique categories from Excel
        excel_categories = df['Category'].unique()

        for category_name in excel_categories:
            try:
                # Generate slug
                slug = category_name.lower()
                slug = re.sub(r'[^a-z0-9\s-]', '', slug)
                slug = re.sub(r'[-\s]+', '-', slug)
                slug = slug[:200]

                # Create or get category
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={
                        'slug': slug,
                        'description': f'{category_name} crackers',
                        'is_active': True
                    }
                )

                category_mapping[category_name] = category
                if created:
                    self.stdout.write(f"Created category: {category_name}")
                else:
                    self.stdout.write(f"Using existing category: {category_name}")

            except Exception as e:
                self.stdout.write(f"Error creating category {category_name}: {e}")

        return category_mapping
