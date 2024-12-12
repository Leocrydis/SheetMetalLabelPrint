import os
from nicegui import app, ui

# Enable JSON indentation for the storage
app.storage.general.indent = True


def find_lst_files(folder_path):
    """Returns a list of `.lst` files with `_1` stripped from their names."""
    lst_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.lst'):  # Match .lst case-insensitively
                # Strip `_1` from the end of the filename if it exists
                clean_name = file.replace('_1.LST', '.LST').replace('_1.lst', '.lst')
                lst_files.append(clean_name)
    return lst_files


def compare_lst_with_sink_configuration(lst_files):
    """
    Compares the provided `.lst` file names with the `sink_combined_configuration`
    in the XML data table stored in NiceGUI's app storage.
    Additionally, counts and tracks XML configurations missing their `.lst` programs.
    """
    # Retrieve XML data table from the app's storage
    xml_data = app.storage.general.get('xml_table', [])

    # Safely extract `sink_combined_configuration` values from the XML table
    sink_configurations = [
        row.get('sink_combined_configuration') for row in xml_data if 'sink_combined_configuration' in row
    ]

    # Filter out any `None` values (in case some rows don't have this field)
    sink_configurations = [config for config in sink_configurations if config]

    # Strip `.LST` or `.lst` from the `.lst` file names for comparison
    lst_files_stripped = [file.rsplit('.', 1)[0] for file in lst_files]  # Remove the extension

    # Compare `.lst` file names against the sink configurations
    matched_sinks = [file for file, stripped in zip(lst_files, lst_files_stripped) if stripped in sink_configurations]
    unmatched_sinks = [file for file, stripped in zip(lst_files, lst_files_stripped) if stripped not in sink_configurations]

    # New logic: Find configurations in the XML that are missing corresponding `.lst` files
    missing_programs = [config for config in sink_configurations if config not in lst_files_stripped]

    # Log or save the comparison results to general storage
    app.storage.general['matched_sinks'] = matched_sinks
    app.storage.general['unmatched_sinks'] = unmatched_sinks  # Storing only the list of unmatched `.lst`
    app.storage.general['missing_programs'] = {
        'list': missing_programs,  # List of missing XML configurations
        'count': len(missing_programs)  # Count of missing programs
    }


@ui.refreshable
def process_sink_folder_reference(folder_path="Z:\\PUNCH\\SINKS\\Form Only"):
    """
    Processes a folder to find `.lst` files and compare them with the sink configuration
    in the XML data table.
    """
    # Find all `.lst` files in the folder
    lst_files = find_lst_files(folder_path)

    if not lst_files:
        print(f"No .lst files found in the folder: {folder_path}")
        return []

    # Save the list of `.lst` files to the app's storage
    app.storage.general['form_only_sinks'] = lst_files

    # Compare `.lst` files with the XML sink configurations
    compare_lst_with_sink_configuration(lst_files)

    # Debugging outputs
    print(f"Found .lst files: {lst_files}")
    print(f"Matched Sinks: {app.storage.general.get('matched_sinks', [])}")
    print(f"Unmatched Sinks: {app.storage.general.get('unmatched_sinks', [])}")

    return lst_files
