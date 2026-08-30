#!/usr/bin/env python3
"""Export products without `main_image` to `unmatched_products.csv`"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

import csv
from products.models import Product
from django.conf import settings

out = os.path.join(settings.BASE_DIR, 'unmatched_products.csv')
with open(out, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'sku', 'category', 'has_image'])
    for p in Product.objects.all():
        writer.writerow([p.name, getattr(p, 'sku', ''), getattr(p.category, 'name', ''), bool(p.main_image)])

print('Wrote', out)
