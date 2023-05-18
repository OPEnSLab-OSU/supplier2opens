import sys
from os import path
import pandas as pd

def validFileExtension(csv_filename, *args):
    return True if csv_filename.split(".")[-1] in args else False

def main():
    DIGIKEY_START_ROW = 3
    MOUSER_START_ROW = 9

    # Handle arguments
    if len(sys.argv) < 2:
        print("ERROR: please provide a file to process...")
        print("USAGE: python digi2opens.py <filename>")
        sys.exit()
    csv_filename = sys.argv[1]
    # Check if file is a csv
    if not validFileExtension(csv_filename, "csv", "xls"):
        print("ERROR: please provide a file with a valid extension...")
        sys.exit()
    # Check if the file exists
    if not path.isfile(csv_filename):
        print(f"ERROR: {csv_filename} does not exist...")
        sys.exit()

    # Get user specific details
    print(f"CSV Path: {csv_filename}")
    suppliers = ["digikey", "mouser"]
    print("Choose the supplier you are using:")
    for idx, supplier in enumerate(suppliers):
        print(f"\t ({idx}) {supplier}")
    while True:
        try: selection = int(input("Selection: "))
        except:
            print("ERROR: please provide a number for your selection...")
            continue
        if selection in range(len(suppliers)):
            supplier = suppliers[selection]
            break
        else: 
            print(f"ERROR: {selection} is not a valid choice...")
            continue
    date_needed = input("Date needed (ASAP or MM/DD/YYYY): ")
    ship_to = input("Ship to (Lab, etc.): ")
    name = input("Name (First Last): ")
    while True:
        try: num = int(input("How many orders of the list? "))
        except:
            print("ERROR: please provide a number...")
            continue
        break

    # Setup output dataframe in opens lab format
    output_cols = ["Date Needed", "Ship To", "Name", "Source", "Description", 
                   "Units", "Part Number", "Price/Unit", "Total"]
    output_df = pd.DataFrame(columns=output_cols)

    # Read and parse CSV contents
    row_data = {}
    row_data["Date Needed"] = date_needed
    row_data["Ship To"] = ship_to
    row_data["Name"] = name

    if supplier == "digikey":
        csv_contents = pd.read_csv(csv_filename, delimiter=",", skiprows=[x for x in range(DIGIKEY_START_ROW - 1)])
        for idx in range(len(csv_contents)):
            row_data["Description"] = csv_contents.loc[idx, "Description"]
            row_data["Units"] = csv_contents.loc[idx, "Requested Quantity 1"] * num
            row_data["Part Number"] = csv_contents.loc[idx, "Digi-Key Part Number 1"]
            row_data["Price/Unit"] = csv_contents.loc[idx, "Unit Price 1"]
            row_data["Total"] = row_data["Units"] * row_data["Price/Unit"]
            row_data["Source"] = f"=HYPERLINK(\"https://www.digikey.com/en/products/result?keywords={row_data['Part Number']}\", \"Digi-Key\")"
            output_df = pd.concat([output_df, pd.DataFrame([row_data])], ignore_index=True)
    elif supplier == "mouser":
        csv_contents = pd.read_excel(csv_filename, skiprows=[x for x in range(MOUSER_START_ROW - 1)], usecols=[x for x in range(1, 11)])
        for idx in range(len(csv_contents)):
            if pd.isna(csv_contents.loc[idx, "Mouser #"]): break
            row_data["Description"] = csv_contents.loc[idx, "Description"]
            row_data["Units"] = csv_contents.loc[idx, "Order Qty."] * num
            row_data["Part Number"] = csv_contents.loc[idx, "Mouser #"]
            row_data["Price/Unit"] = float(csv_contents.loc[idx, "Price (USD)"][1:])
            row_data["Total"] = row_data["Units"] * row_data["Price/Unit"]
            row_data["Source"] = f"=HYPERLINK(\"https://www.mouser.com/ProductDetail/{row_data['Part Number']}\", \"Mouser\")"
            output_df = pd.concat([output_df, pd.DataFrame([row_data])], ignore_index=True)

    print(output_df)

    # Calculate total and per list cost
    total_cost = output_df["Total"].sum()
    print(f"Total cost: ${total_cost:.2f}")
    if num > 1:
        print(f"Cost per list: ${total_cost / num:.2f}")

    # Copy output csv to the clipboad
    output_df.to_clipboard(index=False, header=False)
    print("\nCopied csv to the clipboard...")


if __name__ == "__main__":
    main()
