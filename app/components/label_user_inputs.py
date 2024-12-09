import cairo
from io import BytesIO
from nicegui import ui, app
from app.data import save_data
from nicegui.functions.refreshable import refreshable

customer_location_input = None
job_name_input = None
item_number_input = None
file_path_label = None

tppn_milmat_label = None
part_number_label = None
x_of_y_label = None

@refreshable
def label_inputs_and_preview():
    with ui.splitter().classes('w-full') as splitter:
        with splitter.before:
            with ui.column().classes('w-full p-4'):
                global customer_location_input, job_name_input, item_number_input, file_path_label
                customer_location_input = ui.input(
                    label='Customer Location',
                    on_change=lambda e: (save_data('file_breakdown.customer_location', e.value))
                ).bind_value(app.storage.general['file_breakdown'], 'customer_location').classes('w-full')

                job_name_input = ui.input(
                    label='Job Name',
                    on_change=lambda e: (save_data('file_breakdown.job_name', e.value))
                ).bind_value(app.storage.general['file_breakdown'], 'job_name').classes('w-full')

                item_number_input = ui.input(
                    label='Item Number',
                    on_change=lambda e: (save_data('file_breakdown.item_name', e.value))
                ).bind_value(app.storage.general['file_breakdown'], 'item_name').classes('w-full')

                file_path_label = ui.label().bind_text(app.storage.general['file_breakdown'], target_name='file_path').classes('w-full mt-4')

        with splitter.after:
            with ui.column().classes('w-full p-4').style('padding: 20px;'):
                ui.label('LABEL PREVIEW').classes('font-bold')
                label_preview = ui.card().tight().classes('flex-auto mb-4').style(
                    'width: 4in; height: 1in; border: 2px solid gray; border-radius: 10px; display: flex; align-items: center; justify-content: center; overflow: hidden;')

                with label_preview:
                    with ui.grid(columns=4).classes('w-full gap-0 truncate'):
                        ui.label().bind_text(app.storage.general['file_breakdown'], 'customer_location').classes(
                            'col-span-full mx-auto justify-center items-center').style('font-size: 14px;')
                        ui.label().bind_text(app.storage.general['file_breakdown'], 'job_name').classes('pl-1 col-span-2').style('font-size: 12px;')
                        ui.label().bind_text(app.storage.general['file_breakdown'], 'item_name').classes('col-span-2 flex justify-center items-center').style(
                            'font-size: 14px;')
                        # Example part number and other labels
                        global tppn_milmat_label, part_number_label, x_of_y_label
                        tppn_milmat_label = ui.label('Part # Example').classes('pl-2 col-span-1 text-white bg-black').style('font-size: 12px;')
                        part_number_label = ui.label('Example Part Number').classes(
                            'flex justify-center items-center col-span-3 row-span-2 text-white bg-black').style('font-size: 16px;')
                        x_of_y_label = ui.label('1 of 1').classes('pl-4 col-span-1 bg-black text-white').style('font-size: 10px;')
                        ui.label().bind_text(app.storage.general['file_breakdown'], 'file_path').classes('pl-1 col-span-full mx-auto flex-auto').style(
                            'font-size: 10px')

                def generate_svg() -> str:
                    output = BytesIO()
                    surface = cairo.SVGSurface(output, 288, 72)
                    draw(surface)
                    surface.finish()
                    return output.getvalue().decode('utf-8')

                def draw(surface: cairo.Surface) -> None:
                    context = cairo.Context(surface)
                    context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                    context.set_font_size(20)
                    context.move_to(10, 10)
                    context.show_text(customer_location_input.value)
                    context.move_to(10, 20)
                    context.show_text(job_name_input.value)
                    context.move_to(10, 30)
                    context.show_text(item_number_input.value)

                # New label preview using SVG
                with ui.column():
                    ui.label('SVG LABEL PREVIEW').classes('font-bold')
                    svg_preview = ui.html().classes('border-2 border-gray-500').style('width: 4in; height: 1in;')
                    svg_preview.content = generate_svg()
