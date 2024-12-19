import os
from nicegui import app, ui
from app.utils import select_dxf_file

server_to_drive_mapping = {
    "\\\\fs01\\caddata\\": "M:\\",
    "\\\\fs01\\CADData\\": "M:\\",
    "\\\\fs01\\cadarchive\\": "N:\\",
    "\\\\fs01\\CADArchive\\": "N:\\",
    "\\\\fs01\\cadarchive2\\": "O:\\",
    "\\\\fs01\\CADArchive2\\": "O:\\",
    "\\\\sql01\\Software\\": "S:\\",
    "\\\\fs01\\common\\": "W:\\",
    "\\\\fs01\\engineering\\": "Y:\\",
    "\\\\fs01\\library\\": "Z:\\"
}

def replace_server_string_with_drive(path):
    path_lower = path.lower()
    for server_string, drive in server_to_drive_mapping.items():
        server_string_lower = server_string.lower()
        if path_lower.startswith(server_string_lower):
            return path.replace(server_string, drive)
    return path

catalog = "CATALOG"
chainAccounts = ["OG", "OBS", "LH", "CG", "BB", "RL", "Ruths Chris", "CH", "FPS"]

def breakdown_path(path):
    if ':' in path:
        path = path.split(':', 1)[1]

    parts = path.split('\\')
    num_parts = len(parts)
    customer_location = ""
    location_folder = ""
    item_number = ""
    found_chain_account = False

    if num_parts == 7:
        customer_location = parts[1]
        location_folder = parts[4]
        item_number = parts[5]
    elif num_parts == 6:
        if catalog in path:
            customer_location = parts[1]
            location_folder = parts[2]
            item_number = parts[3]
        else:
            for chain_account in chainAccounts:
                if chain_account in path:
                    customer_location = parts[1]
                    location_folder = parts[3]
                    item_number = parts[4]
                    found_chain_account = True
                    break
            if not found_chain_account:
                customer_location = parts[2]
                location_folder = parts[3]
                item_number = parts[4]
    elif num_parts == 5:
        if catalog in path:
            customer_location = parts[1]
            location_folder = parts[2]
            item_number = ""
        else:
            for chain_account in chainAccounts:
                if chain_account in path:
                    customer_location = parts[1]
                    location_folder = parts[2]
                    item_number = parts[3]
                    found_chain_account = True
                    break
            if not found_chain_account:
                customer_location = parts[1]
                location_folder = parts[2]
                item_number = parts[3]
    elif num_parts == 4:
        if catalog in path:
            customer_location = parts[1]
            location_folder = parts[2]
            item_number = ""
        else:
            for chain_account in chainAccounts:
                if chain_account in path:
                    customer_location = parts[1]
                    location_folder = parts[2]
                    item_number = parts[3]
                    found_chain_account = True
                    break
            if not found_chain_account:
                customer_location = parts[1]
                location_folder = parts[2]
                item_number = parts[3]
    elif num_parts == 3:
        if catalog in path:
            customer_location = parts[1]
            location_folder = parts[2]
            item_number = ""
        else:
            for chain_account in chainAccounts:
                if chain_account in path:
                    customer_location = parts[1]
                    location_folder = parts[2]
                    item_number = parts[3]
                    found_chain_account = True
                    break
            if not found_chain_account:
                customer_location = parts[1]
                location_folder = parts[2]
                item_number = parts[3]

    return customer_location, location_folder, item_number

def check_file_extension():
    file_path = app.storage.general.get('file_path', '')
    file_extension = os.path.splitext(file_path)[1]
    return file_extension, file_path

async def file_path_breakdown():
    data = {}

    # Get the original file path and its extension
    file_extension, original_file_path = check_file_extension()

    # Initialize the file path to the original .xml/.csv/.dxf file path
    file_path = original_file_path

    # If in the specific `M:\\0-BOOST NC\\PR\\PINK-RUSH` directory and it's an .xml file, allow a .dxf selection
    if "M:\\0-BOOST NC\\PR\\PINK-RUSH" in file_path and file_extension == '.xml':
        dxf_file_path = await select_dxf_file()
        if dxf_file_path:
            # Replace server path for the selected .dxf file
            dxf_file_path = replace_server_string_with_drive(dxf_file_path)

            # Use the breakdown of the selected DXF file but retain the original .xml file path
            dxf_customer_location, dxf_job_name, dxf_item_name = breakdown_path(dxf_file_path)

            # Populate the shared fields based on the DXF breakdown
            data.update({
                "file_path": original_file_path,  # Keep the original .xml path
                "customer_location": dxf_customer_location,
                "job_name": dxf_job_name,
                "item_name": dxf_item_name
            })
        else:
            # Notify user if no DXF file was selected
            ui.notify('DXF file selection cancelled', position='center', type='negative')
            return
    else:
        # For other cases, replace server path for the original file
        file_path = replace_server_string_with_drive(file_path)

        # Populate shared fields for XML, CSV, or DXF file directly
        if file_extension in ['.xml', '.csv', '.dxf']:
            customer_location, job_name, item_name = breakdown_path(file_path)
            data.update({
                "file_path": file_path,
                "customer_location": customer_location,
                "job_name": job_name,
                "item_name": item_name
            })

    # Update app storage with the final breakdown data
    app.storage.general['file_breakdown'] = data


