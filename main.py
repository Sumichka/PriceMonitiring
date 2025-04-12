from Silpo import get_silpo
from metro import get_metro
from oil_prices_mapper import merge_data
from build_excel_output import create_excel

if __name__ == "__main__":
    """
    The merged data will contain the prices from both
    Silpo and Metro for each unique product
    based on brand, refinement, and volume.
    """
    # Get data from both sources
    get_silpo()
    get_metro()

    # Merge the data
    merge_data()
    print("Data merged and saved to merged_output.json")
    create_excel()
    print("Excel file 'oil_prices.xlsx' created.")
