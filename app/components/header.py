from nicegui import ui
from .table import data_table
from .label_user_inputs import  label_inputs_and_preview
from app.utils import select_xml_file, select_csv_file
from app.events import file_path_breakdown, run_sink_configuration
from app.resource import process_sink_folder_reference
from app.pages import reports_page

async def xml_file_selection():
    await select_xml_file()
    await file_path_breakdown()
    progress_dialog.open()
    await run_sink_configuration()
    progress_dialog.close()
    ui.timer(interval=0.1, callback=data_table.refresh, once=True)
    ui.timer(interval=0.1, callback=label_inputs_and_preview.refresh, once=True)
    ui.timer(interval=0.1, callback=process_sink_folder_reference.refresh, once=True)

async def csv_file_selection():
    await select_csv_file()
    await file_path_breakdown()
    ui.timer(interval=0.1, callback=data_table.refresh, once=True)
    ui.timer(interval=0.1, callback=label_inputs_and_preview.refresh, once=True)

def header_component():
    with ui.row().classes('w-full m-4'):
        with ui.button(icon='menu').classes('h-14'):
            ui.tooltip('Menu').classes('bg-green')
            with ui.menu() as menu:
                ui.menu_item('Settings').props('icon=folder_open')
                ui.menu_item('Close', menu.close())

        with ui.button(text='Select File', icon='folder_open').classes('h-14'):
            with ui.menu():
                with ui.menu_item(on_click=xml_file_selection).props():
                    ui.avatar(icon='file_open')
                    ui.label('XML File').classes('my-auto ml-2')
                with ui.menu_item(on_click=csv_file_selection).props():
                    ui.avatar(icon='file_open')
                    ui.label('CSV File').classes('my-auto ml-2')

        with ui.button(icon='work_history', on_click= reports_page).classes('ml-auto h-14'):
            ui.tooltip('View reports').classes('bg-green')
            ui.badge(text='0', color='red').props('floating')

        # Display the progress dialog
        global progress_dialog
        with ui.dialog().props('persistent') as progress_dialog:
            with ui.card().style('width: 200px; height: 200px; display: flex; align-items: center; justify-content: center;'):
                ui.spinner(size='lg')
                ui.label('Processing...').classes('mt-4')