#!/usr/bin/env python3
"""Scrape BabyCrackers product list (name, price, image URL)

Requires Playwright. Run:
  .\venv\Scripts\python.exe -m pip install playwright
  .\venv\Scripts\python.exe -m playwright install chromium
Then run this script with the venv python.
"""
import json
import csv
import sys
from pathlib import Path

URL = 'https://www.babycrackers.com/#/productlist'


def run():
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        print('Playwright not installed. See top of file for install instructions.')
        raise

    out_dir = Path(__file__).parent
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_load_state('networkidle', timeout=60000)

        # Evaluate heuristics in page to extract product-like items
        items = page.evaluate("""
        () => {
            const imgs = Array.from(document.querySelectorAll('img'));
            const seen = new Set();
            const out = [];
            imgs.forEach(img => {
                const src = img.src || img.getAttribute('data-src') || '';
                if (!src) return;
                if (seen.has(src)) return;
                seen.add(src);

                // find closest container
                let el = img.closest('article, li, div') || img.parentElement;
                // name heuristics
                let nameEl = el && el.querySelector('h1,h2,h3,h4,.title,.name,.product-name');
                let priceEl = el && el.querySelector('.price,.product-price,.amount');
                // fallback: look for sibling text nodes
                let name = nameEl ? nameEl.innerText.trim() : (img.alt || '').trim();
                let price = priceEl ? priceEl.innerText.trim() : '';

                // try wider search if empty
                if (!name) {
                    const txt = (el && el.innerText) || '';
                    const lines = txt.split('\n').map(s=>s.trim()).filter(Boolean);
                    if (lines.length) name = lines[0];
                }

                out.push({name, price, src});
            });
            return out;
        }
        """)

        # dedupe by src
        by_src = {}
        for it in items:
            src = it.get('src')
            name = it.get('name','').strip()
            price = it.get('price','').strip()
            if src in by_src:
                # prefer longer name/price
                if len(name) > len(by_src[src]['name']):
                    by_src[src]['name'] = name
                if len(price) > len(by_src[src]['price']):
                    by_src[src]['price'] = price
            else:
                by_src[src] = {'name': name, 'price': price, 'src': src}

        products = list(by_src.values())

        # close
        browser.close()

    # write files
    json_path = out_dir / 'babycrackers_products.json'
    csv_path = out_dir / 'babycrackers_products.csv'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name','price','image_url'])
        for p in products:
            writer.writerow([p['name'], p['price'], p['src']])

    print('Wrote', json_path, csv_path)


if __name__ == '__main__':
    run()
