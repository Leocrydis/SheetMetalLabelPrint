import os
from nicegui import ui, app
from app.data import save_data


@ui.refreshable
def label_inputs_and_preview():
    # Get the file path and its extension
    file_path = app.storage.general.get('file_path', '')
    file_extension = os.path.splitext(file_path)[1]

    # Define default label values in case of missing or invalid data
    tppn_milmat_label = "Material"
    part_number_label = "Example Part Number"
    x_of_y_label = "1 of 1"

    # Update label values based on file type and available data
    if file_extension == '.xml':
        xml_data = app.storage.general.get('xml_table', [{}])[0]
        if xml_data:
            tppn_milmat_label = f"Part # {xml_data.get('tops_part_number', '')}" or "Material"
            part_number_label = xml_data.get('unique_code', 'Example Part Number')
            x_of_y_label = xml_data.get('x_of_y', '1 of 1')
    elif file_extension == '.csv':
        csv_data = app.storage.general.get('csv_table', [{}])[0]
        if csv_data:
            tppn_milmat_label = csv_data.get('Material', 'Material')
            part_number_label = csv_data.get('File Name', 'Example Part Number')
            x_of_y_label = csv_data.get('x_of_y', '1 of 1')

    with ui.splitter().classes('w-full') as splitter:
        with splitter.before:
            with ui.column().classes('w-full p-4'):
                # Inputs with bindings
                ui.input(
                    label='Customer Location',
                    on_change=lambda e: save_data('file_breakdown.customer_location', e.value)
                ).bind_value(app.storage.general['file_breakdown'], 'customer_location').classes('w-full')

                ui.input(
                    label='Job Name',
                    on_change=lambda e: save_data('file_breakdown.job_name', e.value)
                ).bind_value(app.storage.general['file_breakdown'], 'job_name').classes('w-full')

                ui.input(
                    label='Item Number',
                    on_change=lambda e: save_data('file_breakdown.item_name', e.value)
                ).bind_value(app.storage.general['file_breakdown'], 'item_name').classes('w-full')

                # Label for `file_path` with default empty value
                ui.label().bind_text(
                    app.storage.general['file_breakdown'], target_name='file_path'
                ).classes('w-full mt-4')

        with splitter.after:
            with ui.column().classes('w-full p-4').style('padding: 20px;'):
                ui.label('LABEL PREVIEW').classes('font-bold')

                # Card simulating label preview
                label_preview = ui.card().tight().classes('flex-auto mb-4').style(
                    'width: 4in; height: 1in; border: 2px solid gray; border-radius: 10px; display: flex; '
                    'align-items: center; justify-content: center; overflow: hidden;'
                )

                with label_preview:
                    with ui.grid(columns=4).classes('w-full gap-0 truncate'):
                        # Labels inside label preview with default fallback behavior
                        ui.label().bind_text(
                            app.storage.general['file_breakdown'], 'customer_location'
                        ).classes('col-span-full mx-auto justify-center items-center').style('font-size: 14px;')

                        ui.label().bind_text(
                            app.storage.general['file_breakdown'], 'job_name'
                        ).classes('pl-1 col-span-2').style('font-size: 12px;')

                        ui.label().bind_text(
                            app.storage.general['file_breakdown'], 'item_name'
                        ).classes('col-span-2 flex justify-center items-center').style('font-size: 14px;')

                        ui.label(tppn_milmat_label
                                 ).classes('pl-2 col-span-1 text-white bg-black').style('font-size: 12px;')

                        ui.label(part_number_label
                                 ).classes('flex justify-center items-center col-span-3 row-span-2 text-white bg-black').style('font-size: 16px;')

                        ui.label(x_of_y_label
                                 ).classes('pl-4 col-span-1 bg-black text-white').style('font-size: 10px;')

                        ui.label().bind_text(
                            app.storage.general['file_breakdown'], 'file_path'
                        ).classes('pl-1 col-span-full mx-auto flex-auto').style('font-size: 10px')