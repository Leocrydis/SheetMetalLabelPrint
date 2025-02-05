from nicegui import ui
from app.components import header_component, label_inputs_and_preview, data_table
from app.resource import process_sink_folder_reference
from app.data import load_data

def startup():
    load_data()
    @ui.page('/')
    async def index():
        # Run the main GUI
        with ui.row().classes('w-full h-full bg-gray-100'):
            header_component()
        with ui.row().classes('w-full h-full bg-gray-100'):
            label_inputs_and_preview()
        with ui.row().classes('w-full h-full bg-gray-100'):
            await data_table()
