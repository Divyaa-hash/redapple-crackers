import json

data = json.load(open('products_fixture.json'))
print('Total products:', len(data))
print('\nProducts with Cloudinary URLs:')
count = 0
for p in data:
    if p['fields']['main_image'] and str(p['fields']['main_image']).startswith('http'):
        count += 1
        if count <= 10:
            name = p['fields']['name']
            image = str(p['fields']['main_image'])[:60]
            print(f"{count}. {name[:40]}: {image}...")

print(f'\nTotal with Cloudinary URLs: {count}')
print(f'Total without images: {sum(1 for p in data if not p["fields"]["main_image"])}')
