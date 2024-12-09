import os
import csv
from tabulate import tabulate
from nicegui import app

def extract_data_from_csv(func):
    async def wrapper(*args, **kwargs):
        csv_content = await func(*args, **kwargs)

        if not csv_content:
            print("No CSV content provided.")
            return []

        # Convert CSV content to a list of lines for the DictReader
        csv_lines = csv_content.splitlines()

        # Skip the first line
        csv_lines = csv_lines[1:]

        # Create the DictReader with the remaining lines
        csv_reader = csv.DictReader(csv_lines)

        table_data = []  # Ensure table_data is initialized

        for i, row in enumerate(csv_reader):
            try:
                quantity = int(row.get('Quantity', 0))
                file_name = row.get('File Name', '')
                title = row.get('Title', '')
                thickness = row.get('Thickness', '')
                material = row.get('Material', '')
                cut_size_x = row.get('Flat_Pattern_Model_CutSizeX', '')
                cut_size_y = row.get('Flat_Pattern_Model_CutSizeY', '')

                # Remove file extension if it is .psm or .par
                base_name, ext = os.path.splitext(file_name)
                if ext in ['.psm', '.par']:
                    file_name = base_name

                # Add multiple lines if quantity is between 2 and 4
                if 1 < quantity <= 4:
                    for j in range(1, quantity + 1):
                        csv_data = {
                            'Quantity': quantity,
                            'File Name': file_name,
                            'Title': title,
                            'Material Thickness': thickness,
                            'Material': material,
                            'Flat_Pattern_Model_CutSizeX': cut_size_x,
                            'Flat_Pattern_Model_CutSizeY': cut_size_y,
                            'x_of_y': f'{j} of {quantity}'
                        }
                        table_data.append(csv_data)
                else:
                    csv_data = {
                        'Quantity': quantity,
                        'File Name': file_name,
                        'Title': title,
                        'Material Thickness': thickness,
                        'Material': material,
                        'Flat_Pattern_Model_CutSizeX': cut_size_x,
                        'Flat_Pattern_Model_CutSizeY': cut_size_y,
                        'x_of_y': f'1 of {quantity}'
                    }
                    table_data.append(csv_data)

            except Exception as row_error:
                print(f"Error processing row: {row}, Error: {row_error}")

        # Print the data for verification
        print(tabulate(table_data))

        # Enable JSON indentation for the storage
        app.storage.general.indent = True
        # Store the data into app.storage.general
        app.storage.general['csv_table'] = table_data

        return table_data  # Return the parsed csv_data

    return wrapper
