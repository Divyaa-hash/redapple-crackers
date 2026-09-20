import os

static_dir = 'static/images/crackers'
if os.path.exists(static_dir):
    images = os.listdir(static_dir)
    print(f'Total static images: {len(images)}')
    print('\nFirst 20 images:')
    for img in sorted(images)[:20]:
        print(f'  - {img}')
