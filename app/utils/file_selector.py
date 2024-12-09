from nicegui import app, ui
from app.data import extract_nc_programs, extract_data_from_csv

@extract_nc_programs
async def select_xml_file():
    # The file dialog returns a tuple where the first item is the path
    selected_file = await app.native.main_window.create_file_dialog(file_types=('XML File (*.xml)',))

    if not selected_file:
        ui.notify('No file Selected', position='center', type='negative')
        return None

    # Unpack the tuple to get the file path
    file_path = selected_file[0] if isinstance(selected_file, tuple) else selected_file

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        ui.notify(f'XML File Loaded: {file_path}', position='center', type='positive')

        app.storage.general.indent = True  # Enable JSON indentation for the storage
        app.storage.general['file_path'] = file_path  # Store the sorted data into app storage

        return xml_content  # unpack and return content inside the file_path

    except Exception as e:
        ui.notify('Failed to open file', position='center', type='negative')
        print(f"Failed to read file: {e}")
        return None

@extract_data_from_csv
async def select_csv_file():
    selected_file = await app.native.main_window.create_file_dialog(file_types=('CSV File (*.csv)',))

    if not selected_file:
        ui.notify('No file Selected', position='center', type='negative')
        return None

    file_path = selected_file[0] if isinstance(selected_file, tuple) else selected_file

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            csv_content = file.read()
        ui.notify(f'CSV File Loaded: {file_path}', position='center', type='positive')

        app.storage.general.indent = True  # Enable JSON indentation for the storage
        app.storage.general['file_path'] = file_path  # Store the sorted data into app storage

        return csv_content  # unpack and return content inside the file_path

    except Exception as e:
        ui.notify('Failed to open file', position='center', type='negative')
        print(f"Failed to read file: {e}")
        return None


async def select_dxf_file():
    selected_file = await app.native.main_window.create_file_dialog(file_types=('DXF File (*.dxf)',))

    if not selected_file:
        ui.notify('No file Selected', position='center', type='negative')
        return None

    file_path = selected_file[0] if isinstance(selected_file, tuple) else selected_file

    app.storage.general.indent = True  # Enable JSON indentation for the storage
    app.storage.general['dxf_file_path'] = file_path  # Store the sorted data into app storage

    return file_path
