#!/usr/bin/env python3
"""
Assign images from `static/images/crackers` to `Product.main_image` by name match.

Usage:
	python assign_babycrackers_images_all.py [--overwrite]

This script searches the `static/images/crackers` folder for files whose
basename matches or contains the product name (slugified) and assigns the
first reasonable candidate as `main_image` for that `Product`.
"""

import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings
from django.core.files import File

from products.models import Product


def slugify_name(name: str) -> str:
	return (
		name.lower()
		.replace('"', '')
		.replace("'", '')
		.replace(' & ', ' and ')
		.replace(' / ', ' ')
		.replace('/', ' ')
		.replace(',', '')
		.strip()
		.replace(' ', '-')
	)


def find_image_for_product(product_name, image_files):
	slug = slugify_name(product_name)
	# exact match first
	for fn in image_files:
		base = os.path.splitext(fn)[0].lower()
		if base == slug:
			return fn

	# startswith or contains
	candidates = [fn for fn in image_files if os.path.splitext(fn)[0].lower().startswith(slug)]
	if candidates:
		return candidates[0]

	contains = [fn for fn in image_files if slug in os.path.splitext(fn)[0].lower()]
	if contains:
		return contains[0]

	# fallback to word matching
	words = [w for w in slug.split('-') if w]
	for fn in image_files:
		base = os.path.splitext(fn)[0].lower()
		if any(w in base for w in words if len(w) > 2):
			return fn

	return None


def main(overwrite=False):
	images_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers')
	if not os.path.isdir(images_dir):
		print('Images directory not found:', images_dir)
		return

	image_files = sorted(os.listdir(images_dir))
	products = Product.objects.all()

	mapped = 0
	skipped = 0
	unmatched = []

	for p in products:
		has_image = bool(p.main_image)
		if has_image and not overwrite:
			skipped += 1
			continue

		candidate = find_image_for_product(p.name, image_files)
		if not candidate:
			unmatched.append(p.name)
			continue

		source_path = os.path.join(images_dir, candidate)
		try:
			with open(source_path, 'rb') as f:
				p.main_image.save(candidate, File(f), save=True)
			mapped += 1
			print(f"Assigned {candidate} → {p.name}")
		except Exception as e:
			print(f"Failed assigning {candidate} to {p.name}: {e}")

	print(f"\nMapped: {mapped}, Skipped(existing): {skipped}, Unmatched: {len(unmatched)}")
	if unmatched:
		print('Unmatched (sample):', unmatched[:30])


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--overwrite', action='store_true', help='Overwrite existing product images')
	args = parser.parse_args()
	main(overwrite=args.overwrite)