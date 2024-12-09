from nicegui import ui
from .table import data_table
from .label_user_inputs import  label_inputs_and_preview
from app.utils import select_xml_file, select_csv_file
from app.events import file_path_breakdown

async def xml_file_selection():
    await select_xml_file()
    ui.timer(interval=0.1, callback=data_table.refresh, once=True)
    await file_path_breakdown()
    ui.timer(interval=0.1, callback=label_inputs_and_preview.refresh, once=True)

async def csv_file_selection():
    await select_csv_file()
    ui.timer(interval=0.1, callback=data_table.refresh, once=True)
    await file_path_breakdown()
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

        with ui.button(icon='work_history').classes('ml-auto h-14'):
            ui.tooltip('View reports').classes('bg-green')
            badge = ui.badge(text='0', color='red').props('floating')
