import cairo
import os
from pdf2image import convert_from_path
from nicegui import app, ui

OUTPUT_DIR = r"M:\0-BOOST NC\SINK REPORTS"
TEMP_IMAGE_DIR = os.path.join(".nicegui", "temp")  # Store temporary image files in the .nicegui/temp directory

# Ensure the temp image directory exists
os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)


def reports_page():
    """
    Generates the report with up-to-date data, converts it into images, and displays them in a dialog.
    """
    # Retrieve necessary data dynamically
    xml_table = app.storage.general.get("xml_table", [])
    matched_sinks = app.storage.general.get("matched_sinks", [])
    file_path = app.storage.general.get("file_path")

    # Step 1: Generate the PDF
    pdf_path = generate_pdf(xml_table, matched_sinks, file_path)

    # Step 2: Convert PDF to images
    image_paths = convert_pdf_to_images(pdf_path, TEMP_IMAGE_DIR)

    # Step 3: Create and display the dialog with images
    with ui.dialog() as report_dialog:
        with ui.card().style('width: 612px; height: 792px;').classes("p-4"):
            # Display each page of the PDF as an image
            for image_path in image_paths:
                ui.image(image_path).style("width: 100%; height: auto; margin-bottom: 10px;")
            ui.button("Close", on_click=lambda: [report_dialog.close(), cleanup_temp_images(TEMP_IMAGE_DIR)]).classes("mt-4")

    # Open the dialog
    return report_dialog


# Modify `generate_pdf` to accept dynamically fetched data
def generate_pdf(xml_table, matched_sinks, file_path) -> str:
    """
    Generates the PDF file using the provided data and returns the file path.
    """
    pdf_path = os.path.join(TEMP_IMAGE_DIR, "sink_configuration_report.pdf")
    with open(pdf_path, "wb") as f:
        surface = cairo.PDFSurface(f, 612, 792)
        draw(surface, xml_table, matched_sinks, file_path)
        surface.finish()
    return pdf_path


# Modify `draw` to accept dynamic data
def draw(surface, xml_table, matched_sinks, file_path):
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

    # Filter rows to include only those with a defined `sink_combined_configuration`
    filtered_xml_table = [row for row in xml_table if row.get("sink_combined_configuration")]

    for row in filtered_xml_table:
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


def convert_pdf_to_images(pdf_path: str, output_dir: str) -> list[str]:
    """
    Converts the PDF at the given path to images, saving them to the output directory.
    Returns the list of image file paths.
    """
    # Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=150)  # Higher DPI for better quality

    # Save the images to the output directory
    image_paths = []
    for i, page in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{i + 1}.png")
        page.save(image_path, "PNG")
        image_paths.append(image_path)

    return image_paths


def cleanup_temp_images(output_dir: str):
    """
    Clears all files in the temporary image directory.
    """
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)