import json

with open('products_fixture.json', 'r') as f:
    data = json.load(f)

print(f'Total products in fixture: {len(data)}')
with_image = sum(1 for p in data if p['fields'].get('image_url'))
without_image = sum(1 for p in data if not p['fields'].get('image_url'))
print(f'With image_url: {with_image}')
print(f'Without image_url: {without_image}')

if without_image > 0:
    print('\nProducts without image_url in fixture:')
    for p in data:
        if not p['fields'].get('image_url'):
            print(f"  - {p['fields']['name']}")
