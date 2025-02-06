import os
from nicegui import app, ui
from app.utils import create_ss_label, create_twob_label, print_label, create_lst_label, check_lst_file_exists, create_qr_label

sheet_repeat_print = True
def check_file_extension():
    # Get file path from storage and parse the file extension
    file_path = app.storage.general.get('file_path', '')
    file_extension = os.path.splitext(file_path)[1]
    return file_extension


@ui.refreshable
async def data_table():

    with ui.row().classes('w-full mx-4'):
        ui.button('Print All', on_click=on_print_all).classes('bg-green-500 text-white rounded')
        ui.button('Print Selected', on_click=on_print_selected).classes('bg-green-500 text-white rounded')
        ui.switch('Repeat Print', value=True, on_change=lambda e: (globals().update(sheet_repeat_print=e.value), ui.notify(str(e.value))))

        ui.button('Laser Sticker', on_click=print_lst_label).classes('ml-auto pr-2')

    # Define the columns for the grid
    xml_columns = [
        {'headerName': 'Program Number', 'field': 'program_number', 'checkboxSelection': True},
        {'headerName': 'Runs', 'field': 'total_number_of_runs'},
        {'headerName': 'Sheet', 'field': 'sheet'},
        {'headerName': 'Part Number', 'field': 'part_number'},
        {'headerName': 'Tops Part Number', 'field': 'tops_part_number'},
        {'headerName': 'Quantity', 'field': 'quantity_on_sheet'},
        {'headerName': 'X of Y', 'field': 'x_of_y'},
        {'headerName': 'Sink Config', 'field': 'sink_combined_configuration', 'hide': False},
        {'headerName': 'Nomex Layers', 'field': 'Nomex Layers', 'hide': False},
    ]

    csv_columns = [
        {'headerName': 'Quantity', 'field': 'Quantity', 'checkboxSelection': True},
        {'headerName': 'File Name', 'field': 'File Name'},
        {'headerName': 'Material', 'field': 'Material'},
        {'headerName': 'X of Y', 'field': 'x_of_y'},
    ]

    # Create the grid outside the function
    global ag_grid  # Declare ag_grid as global to ensure it is accessible in other functions
    ag_grid = ui.aggrid(
        options={
            'columnDefs': [],
            'rowData': [],
            'domLayout': 'autoHeight',
            'rowSelection': 'multiple',
        }
    ).classes('w-full h-full mx-4 bg-gray-100')
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


def get_printer(sheet):
    file_extension = check_file_extension()
    if sheet.startswith("SS-"):
        return "SS"
    elif sheet.startswith("2B-") or sheet.startswith("GL-") or sheet.startswith("ST-") or sheet.startswith("SS-0250-") or sheet.startswith("SS MILL-0187-") or sheet.startswith("SS MILL-0250") or sheet.startswith("SS MILL-0375-"):
        return "2B"
    elif file_extension == '.csv':
        return "CSV"
    else:
        return "Other"

async def on_print_all():
    file_extension = check_file_extension()
    table_data = app.storage.general.get('xml_table', []) if file_extension == '.xml' else app.storage.general.get('csv_table', [])
    zpl_commands = []

    data_type = 'xml' if file_extension == '.xml' else 'csv'
    total_labels = len(table_data)

    # Check for the .lst file only if the file extension is .xml
    if file_extension == '.xml' and check_lst_file_exists():
        lst_zpl_command = create_lst_label()
        zpl_commands.append(lst_zpl_command)
    elif file_extension == '.xml':
        ui.notify('No .lst file exists', position='center', type='warning')

    if file_extension == '.xml' and sheet_repeat_print:
        # Group labels by sheet number (last part of program_number)
        grouped_labels = {}
        for data in table_data:
            program_number = data.get('program_number')
            sheet_number = program_number.rsplit('_', 1)[-1]  # Extract the sheet number
            if sheet_number not in grouped_labels:
                grouped_labels[sheet_number] = []
            grouped_labels[sheet_number].append(data)

        # Create labels for each group and repeat based on total_number_of_runs
        for sheet_number, labels in grouped_labels.items():
            single_run_commands = []
            for data in labels:
                # Determine the label type and create the label accordingly
                label_type = get_printer(data.get('sheet', '2B'))  # Handle missing 'sheet'
                if 'sink_combined_configuration' in data and data['sink_combined_configuration']:
                    zpl_command = create_qr_label(data, data_type, total_labels)
                elif label_type == "SS":
                    zpl_command = create_ss_label(data, data_type, total_labels)
                else:  # Default to 2B
                    zpl_command = create_twob_label(data, data_type)
                single_run_commands.append(zpl_command)

            # Get the total_number_of_runs for the group
            total_runs = int(labels[0].get('total_number_of_runs', 1))
            for _ in range(total_runs):
                zpl_commands.extend(single_run_commands)
    else:
        for data in table_data:
            # Determine the label type and create the label accordingly
            label_type = get_printer(data.get('sheet', '2B'))  # Handle missing 'sheet'
            if 'sink_combined_configuration' in data and data['sink_combined_configuration']:
                zpl_command = create_qr_label(data, data_type, total_labels)
            elif label_type == "SS":
                zpl_command = create_ss_label(data, data_type, total_labels)
            else:  # Default to 2B
                zpl_command = create_twob_label(data, data_type)
            zpl_commands.append(zpl_command)

    # Concatenate all ZPL commands into a single string
    all_zpl_commands = ''.join(zpl_commands)

    # Determine the label type based on the sheet value
    if table_data:
        if file_extension == '.xml':
            label_type = get_printer(table_data[0].get('sheet', '2B'))  # Handle missing 'sheet'
        else:
            label_type = "2B"  # Always print CSV data to the 2B printer
        # Print all labels in one go
        print_label(all_zpl_commands, label_type)


async def on_print_selected():
    file_extension = check_file_extension()
    selected_rows = await ag_grid.get_selected_rows()
    zpl_commands = []

    data_type = 'xml' if file_extension == '.xml' else 'csv'
    total_labels = len(selected_rows)

    if file_extension == '.xml' and sheet_repeat_print:
        # Group labels by sheet number (last part of program_number)
        grouped_labels = {}
        for data in selected_rows:
            program_number = data.get('program_number')
            sheet_number = program_number.rsplit('_', 1)[-1]  # Extract the sheet number
            if sheet_number not in grouped_labels:
                grouped_labels[sheet_number] = []
            grouped_labels[sheet_number].append(data)

        # Create labels for each group and repeat based on total_number_of_runs
        for sheet_number, labels in grouped_labels.items():
            single_run_commands = []
            for data in labels:
                # Determine the label type and create the label accordingly
                label_type = get_printer(data.get('sheet', '2B'))  # Use default '2B' for missing 'sheet'
                if 'sink_combined_configuration' in data and data['sink_combined_configuration']:
                    zpl_command = create_qr_label(data, data_type, total_labels)
                elif label_type == "SS":
                    zpl_command = create_ss_label(data, data_type, total_labels)
                else:  # Default to 2B
                    zpl_command = create_twob_label(data, data_type)
                single_run_commands.append(zpl_command)

            # Get the total_number_of_runs for the group
            total_runs = int(labels[0].get('total_number_of_runs', 1))
            for _ in range(total_runs):
                zpl_commands.extend(single_run_commands)
    else:
        for data in selected_rows:
            # Determine the label type and create the label accordingly
            label_type = get_printer(data.get('sheet', '2B'))  # Use default '2B' for missing 'sheet'
            if 'sink_combined_configuration' in data and data['sink_combined_configuration']:
                zpl_command = create_qr_label(data, data_type, total_labels)
            elif label_type == "SS":
                zpl_command = create_ss_label(data, data_type, total_labels)
            else:  # Default to 2B
                zpl_command = create_twob_label(data, data_type)
            zpl_commands.append(zpl_command)

    # Concatenate all ZPL commands into a single string
    all_zpl_commands = ''.join(zpl_commands)
    print("All ZPL Commands:")
    print(all_zpl_commands)

    # Determine the label type based on the sheet value
    if selected_rows:
        if file_extension == '.xml':
            label_type = get_printer(selected_rows[0].get('sheet', '2B'))  # Handle missing 'sheet'
        else:
            label_type = "2B"  # Always print CSV data to the 2B printer
        # Print all selected labels in one go
        print_label(all_zpl_commands, label_type)


async def print_lst_label():
    lst_zpl_command = create_lst_label()
    print_label(lst_zpl_command, "SS")