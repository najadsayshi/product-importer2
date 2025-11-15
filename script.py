import csv
import random
import uuid

# Number of rows you want
TOTAL_ROWS = 499999

# Output file
OUTPUT_FILE = "products.csv"

# Column headers
headers = ["sku", "name", "description", "price"]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    for i in range(TOTAL_ROWS):
        sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        name = f"Product {i+1}"
        description = f"Description for product {i+1}"
        price = round(random.uniform(10, 999), 2)

        writer.writerow([sku, name, description, price])

print(f"CSV file generated: {OUTPUT_FILE}")
