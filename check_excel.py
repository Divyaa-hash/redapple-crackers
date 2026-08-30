import pandas as pd

# Load Excel file
excel_path = 'Vamsi_Crackers 2026 diwali.xlsx'
df = pd.read_excel(excel_path)

print(f'Total products in Excel: {len(df)}')
print(f'\nCategories in Excel:')
print(df['Category'].unique())

print(f'\nGift Box products in Excel:')
gift_boxes = df[df['Category'].str.contains('GIFT BOX', case=False, na=False)]
print(f'  Total gift boxes: {len(gift_boxes)}')
for index, row in gift_boxes.iterrows():
    print(f'  {index + 1}. {row["Product Name"]} - Status: {row["Status"]}')

print(f'\nFamily Pack products in Excel:')
family_packs = df[df['Category'].str.contains('FAMILY PACK', case=False, na=False)]
print(f'  Total family packs: {len(family_packs)}')
for index, row in family_packs.iterrows():
    print(f'  {index + 1}. {row["Product Name"]} - Status: {row["Status"]}')

print(f'\nFirst 175 products:')
for index, row in df.head(175).iterrows():
    if 'GIFT BOX' in str(row['Category']) or 'FAMILY PACK' in str(row['Category']):
        print(f'  {index + 1}. {row["Product Name"]} - Category: {row["Category"]} - Status: {row["Status"]}')
