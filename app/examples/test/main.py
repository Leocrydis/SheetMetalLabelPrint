from nicegui import ui, app

def dialog_1():
    # Dialog for viewing the report
    with ui.dialog() as report_dialog:
        with ui.card().classes('p-4').style('width: 650px; max-width: 90%;'):
            # Display the SVG preview inside a bordered HTML container
            report_preview = ui.html().classes('border-2 border-gray-500 rounded-md mb-2').style('width: 612px; height: 792px;')

    report_dialog.open()

def dialog_2():
    with ui.dialog() as pdf_dialog:
        with ui.card().style("width: 700px; height: 600px; overflow-y: auto;").classes("p-4"):
            # Display each page of the PDF as an image
                ui.image("image_path").style("max-width: 100%; height: auto; margin-bottom: 10px;")

    pdf_dialog.open()

with ui.row().classes('w-full m-4'):
    with ui.button(icon='menu').classes('h-14'):
        ui.tooltip('Menu').classes('bg-green')
        with ui.menu() as menu:
            ui.menu_item('View PDF', on_click= lambda: dialog_2()).props('icon=page_view')
            ui.menu_item('Settings').props('icon=folder_open')
            ui.menu_item('Close', menu.close())

    with ui.button(text='Select File', icon='folder_open').classes('h-14'):
        with ui.menu():
            with ui.menu_item(on_click='xml_file_selection').props():
                ui.avatar(icon='file_open')
                ui.label('XML File').classes('my-auto ml-2')
            with ui.menu_item(on_click='csv_file_selection').props():
                ui.avatar(icon='file_open')
                ui.label('CSV File').classes('my-auto ml-2')

    ui.button(icon='work_history', on_click=lambda: dialog_1()).classes('h-14')

ui.run(native=True, reload=False)
