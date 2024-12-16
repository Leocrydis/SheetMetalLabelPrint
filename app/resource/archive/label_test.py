import os
import cairo
from io import BytesIO
from nicegui import ui

# Define the base directory for output files (two levels above the current file)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Two levels up
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')  # Subdirectory for outputs

# Ensure the directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Function to generate SVG content
def generate_svg() -> str:
    output = BytesIO()
    surface = cairo.SVGSurface(output, 288, 72)
    draw(surface)
    surface.finish()
    return output.getvalue().decode('utf-8')


# Function to generate PDF (returns the file path to the saved PDF)
def generate_pdf() -> str:
    pdf_path = os.path.join(OUTPUT_DIR, 'label_preview.pdf')  # Define the output path
    with open(pdf_path, 'wb') as f:
        surface = cairo.PDFSurface(f, 288, 72)  # Create and save directly to the file
        draw(surface)  # Draw the content on the surface
        surface.finish()  # Finalize the surface
    return pdf_path  # Return the file path to the PDF


# Function to draw the label content (common for both SVG and PDF)
def draw(surface: cairo.Surface) -> None:
    context = cairo.Context(surface)  # Create a drawing context
    context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(12)
    # Draw text elements at specified positions
    context.move_to(10, 20)  # customer location
    context.show_text('customer_location')
    context.move_to(10, 40)  # job name
    context.show_text('job_name')
    context.move_to(250, 40)  # item number
    context.show_text('item_number')
    context.move_to(10, 50)  # tppn/milmat
    context.show_text('tppn_milmat_label')
    context.move_to(150, 60)  # part number
    context.show_text('part_number_label')
    context.move_to(10, 60)  # x of y
    context.show_text('x_of_y_label')
    context.move_to(10, 70)  # file path
    context.show_text('file_path_label')


# Show SVG Preview
with ui.column():
    ui.label('SVG LABEL PREVIEW').classes('font-bold')
    svg_preview = ui.html().classes('border-2 border-gray-500').style('width: 288px; height: 72px;')
    svg_preview.content = generate_svg()

# PDF Download Button
ui.button('Download PDF', on_click=generate_pdf)