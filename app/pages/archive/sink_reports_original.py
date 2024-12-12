import cairo
import os
from io import BytesIO
from nicegui import app, ui

# Retrieve necessary data from storage
xml_table = app.storage.general.get('xml_table', [])
matched_sinks = app.storage.general.get('matched_sinks', [])
file_path = app.storage.general.get('file_path')

OUTPUT_DIR = r"M:\0-BOOST NC\SINK REPORTS"


def reports_page():
    """
    Generates and displays the reports page inside a dialog.
    """
    # Dialog for viewing the report
    with ui.dialog() as report_dialog:
        with ui.card().classes('p-4').style('width: 650px; max-width: 90%;'):
            # Display the SVG preview inside a bordered HTML container
            report_preview = ui.html().classes('border-2 border-gray-500 rounded-md mb-2').style('width: 612px; height: 792px;')
            report_preview.content = generate_svg()

            # Print Button
            ui.button('Export Report', on_click=lambda: generate_pdf()).classes('mt-2')

    return report_dialog


# Function to draw the content of the report
def draw(surface):
    context = cairo.Context(surface)

    # Define layout sizes
    page_width, page_height = 612, 792  # Letter size in points
    margin = 20

    # Fonts
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(18)

    # Header
    context.move_to(margin, 40)
    context.show_text("REPORT: Sink Configuration")

    # XML File Path Section
    context.set_font_size(12)
    context.move_to(margin, 60)
    context.show_text(f"File Path: {file_path}")

    # Draw Table Headers
    column_width = (page_width - 2 * margin) // 3
    context.move_to(margin, 100)
    context.set_font_size(14)
    context.show_text("Part Number")
    context.move_to(margin + column_width, 100)
    context.show_text("Sink Config")
    context.move_to(margin + 2 * column_width, 100)
    context.show_text("Lst File")

    # Draw Table Content
    context.set_font_size(12)
    y_offset = 120
    row_height = 20
    for row in xml_table:
        # Get data for each row
        part_number = row.get("part_number", "N/A")
        sink_config = row.get("sink_combined_configuration", "N/A")
        lst_file = next((f for f in matched_sinks if sink_config in f), "N/A")

        # Draw each column
        context.move_to(margin, y_offset)
        context.show_text(str(part_number))
        context.move_to(margin + column_width, y_offset)
        context.show_text(str(sink_config))
        context.move_to(margin + 2 * column_width, y_offset)
        context.show_text(lst_file)

        # Move to the next row
        y_offset += row_height


# Function to generate SVG content
def generate_svg() -> str:
    output = BytesIO()
    surface = cairo.SVGSurface(output, 612, 792)  # Letter size in points
    draw(surface)
    surface.finish()
    return output.getvalue().decode('utf-8')


# Function to generate PDF (returns the file path to the saved PDF)
def generate_pdf() -> str:
    pdf_path = os.path.join(OUTPUT_DIR, 'sink_configuration_report.pdf')  # Define the output path
    with open(pdf_path, 'wb') as f:
        surface = cairo.PDFSurface(f, 612, 792)  # Letter size in points
        draw(surface)
        surface.finish()
    return pdf_path  # Return the file path to the PDF

