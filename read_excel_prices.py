import pandas as pd
import sys
import io

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

# Read the Excel file
df = pd.read_excel('Final_Price_List_RAC_2026.xlsx', header=3)

# Filter out category header rows (rows with ★ in S.No column)
df = df[df['S.No'].astype(str).str.contains('★') == False]

# Filter out rows where Category is NaN (these are category headers)
df = df[df['Category'].notna()]

# Drop rows where Name of Product is NaN
df = df[df['Name of Product (English)'].notna()]

# Keep only relevant columns
df = df[['Name of Product (English)', 'Net Rate (₹)']].copy()

# Clean up the data
df['Name of Product (English)'] = df['Name of Product (English)'].str.strip()
df['Net Rate (₹)'] = pd.to_numeric(df['Net Rate (₹)'], errors='coerce')

# Drop rows with no price
df = df[df['Net Rate (₹)'].notna()]

print(f"Total products found: {len(df)}")
print("\nFirst 50 products:")
print(df.head(50).to_string(index=False))

# Save to CSV for easier processing
df.to_csv('price_mapping.csv', index=False)
print("\nSaved to price_mapping.csv")
