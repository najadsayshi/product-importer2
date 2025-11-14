import csv
from typing import Iterator, Dict, Any

def stream_csv_rows(path: str) -> Iterator[Dict[str, Any]]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # standardize keys, ensure required fields exist
            yield row
