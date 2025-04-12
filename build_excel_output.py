import json
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def create_excel():
    # Load merged data
    with open('merged_output.json', encoding='utf-8') as f:
        merged_data = json.load(f)

    # Prepare rows
    rows = []
    for item in merged_data:
        full_name = f"{item['brand'].capitalize()}, {item['refinement']} {item['volume']}"
        rows.append({
            "Назва олії": full_name,
            "Ціна Silpo": item.get("price_file1"),
            "Ціна Metro": item.get("price_file2")
        })

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Oil Prices"

    # Add DataFrame rows to worksheet
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Add empty row + footer timestamp
    ws.append([])
    ws.append([f"Created at: {datetime.now().strftime('%Y-%m-%d')}"])

    # Save final Excel
    wb.save(f"oil_prices_{datetime.now().strftime('%Y-%m-%d')}.xlsx")

    print("Excel file 'oil_prices.xlsx' created with timestamp in the footer.")