import os
from pdf2image import convert_from_path
from nicegui import app, ui

TEMP_IMAGE_DIR = os.path.join(".nicegui", "temp")  # Store temporary image files in the .nicegui/temp directory

# Ensure the temp image directory exists
os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)


async def select_pdf_file():
    """
    Opens a file dialog for selecting a PDF file and returns the selected file's path.
    """
    # File dialog for PDF files
    selected_file = await app.native.main_window.create_file_dialog(file_types=('PDF File (*.pdf)',))

    if not selected_file:
        ui.notify('No file selected', position='center', type='negative')
        return None

    # Unpack the tuple to get the file path
    pdf_path = selected_file[0] if isinstance(selected_file, tuple) else selected_file

    return pdf_path


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


async def pdf_previewer():
    """
    Prompts the user to select a PDF, converts it into images, and displays them in a dialog.
    """
    # Step 1: Prompt the user to select a PDF file
    pdf_path = await select_pdf_file()

    if not pdf_path:
        return  # No file was selected

    # Step 2: Convert PDF to images
    image_paths = convert_pdf_to_images(pdf_path, TEMP_IMAGE_DIR)

    # Step 3: Create and display the dialog with images
    with ui.dialog() as pdf_dialog:
        with ui.card().style("width: 700px; height: 600px; overflow-y: auto;").classes("p-4"):
            # Display each page of the PDF as an image
            for image_path in image_paths:
                ui.image(image_path).style("max-width: 100%; height: auto; margin-bottom: 10px;")
            # Close button to exit and clean up temporary files
            ui.button("Close", on_click=lambda: [pdf_dialog.close(), cleanup_temp_images(TEMP_IMAGE_DIR)]).classes("mt-4")

    pdf_dialog.open()