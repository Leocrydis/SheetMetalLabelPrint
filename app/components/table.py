import os
from nicegui import app, ui

def check_file_extension():
    # Get file path from storage and parse the file extension
    file_path = app.storage.general.get('file_path', '')
    file_extension = os.path.splitext(file_path)[1]
    return file_extension

@ui.refreshable
async def data_table():
    # Define the columns for the grid
    xml_columns = [
        {'headerName': 'Program Number', 'field': 'program_number', 'checkboxSelection': True},
        {'headerName': 'Runs', 'field': 'total_number_of_runs'},
        {'headerName': 'Sheet', 'field': 'sheet'},
        {'headerName': 'Part Number', 'field': 'part_number'},
        {'headerName': 'Tops Part Number', 'field': 'tops_part_number'},
        {'headerName': 'Quantity', 'field': 'quantity_on_sheet'},
        {'headerName': 'X of Y', 'field': 'x_of_y'},
        {'headerName': 'Sink Config', 'field': 'sink_combined_configuration', 'hide': False}
    ]

    csv_columns = [
        {'headerName': 'Quantity', 'field': 'Quantity', 'checkboxSelection': True},
        {'headerName': 'File Name', 'field': 'File Name'},
        {'headerName': 'Material', 'field': 'Material'},
        {'headerName': 'X of Y', 'field': 'x_of_y'},
    ]

    # Create the grid outside the function
    ag_grid = ui.aggrid(
        options={
            'columnDefs': [],
            'rowData': [],
            'domLayout': 'autoHeight',
            'rowSelection': 'multiple',
        }
    ).classes('w-full h-full p-4 justify-start gap-4 bg-gray-100')

    file_extension = check_file_extension()

    if file_extension == '.xml':
        ag_grid.options['columnDefs'] = xml_columns
        ag_grid.options['rowData'] = app.storage.general.get('xml_table', [])
        ui.notify('Table updated with xml data', position='center', type='positive')
    elif file_extension == '.csv':
        ag_grid.options['columnDefs'] = csv_columns
        ag_grid.options['rowData'] = app.storage.general.get('csv_table', [])
        ui.notify('Table updated with csv data', position='center', type='positive')
    else:
        ui.notify('No data to display', position='center', type='warning')