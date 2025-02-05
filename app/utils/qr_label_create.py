import zpl
from nicegui import app
import os

def create_label(data, data_type, total_labels):
    # Convert inches to millimeters (1 inch = 25.4 mm)
    label_width_mm = 4 * 25.4  # 4 inches wide
    label_height_mm = 1 * 25.4  # 1 inch tall
    text_width_mm = 3 * 25.4  # 3 inches for text
    qr_code_width_mm = 1 * 25.4  # 1 inch for QR code

    # Create a new label with dimensions in millimeters
    l = zpl.Label(label_height_mm, label_width_mm)

    if total_labels > 25:
        l.zpl_raw("^MMP,N")  # Set the print mode to peel off
    else:
        l.zpl_raw("^MMT")  # Set the print mode to tear off

    # Fetch common data from file_breakdown
    file_breakdown = app.storage.general.get('file_breakdown', {})
    customer_location = file_breakdown.get('customer_location', 'Customer Location')
    job_name = file_breakdown.get('job_name', 'Job Name')
    item_name = file_breakdown.get('item_name', 'Item Number')
    file_path = file_breakdown.get('file_path', 'File Path').replace('\\', '/')

    # Define the text for each row using data from the input
    if data_type == 'xml':
        texts = [
            customer_location,
            job_name,
            item_name,
            f"Part # {data.get('tops_part_number', '')}",
            data.get('x_of_y', 'X of Y'),
            data.get('unique_code', 'Part Number'),
            file_path
        ]
    elif data_type == 'csv':
        texts = [
            customer_location,
            job_name,
            item_name,
            data.get('Material', 'Material'),
            data.get('x_of_y', 'X of Y'),
            data.get('File Name', 'Part Number'),
            file_path
        ]

    # Add the sink_combined_configuration to the left of row 4 if available
    sink_combined_configurations = data.get('sink_combined_configuration', '')
    if sink_combined_configurations:
        texts.insert(0, sink_combined_configurations)

    # Define the y positions for each row (in millimeters)
    y_positions = [2, 7, 7, 13, 18, 13, 24]  # Adjust these values as needed

    # Define the x positions for each column in row 2 (in millimeters)
    x_positions_row2 = [0, text_width_mm - (text_width_mm / 2) - 4]  # Column 1 starts at 0, Column 2 is offset by 4 mm from the right edge

    # Define the x positions for each column in rows 3 and 4 (in millimeters)
    x_positions_row3_4 = [0, 26]  # Column 1 starts at 0, Column 2 starts at 26 mm

    # Add the sink_combined_configuration to the left of row 1 if available
    sink_combined_configuration = data.get('sink_combined_configuration', '')
    if sink_combined_configuration:
        l.origin(26, 18)
        l.write_text(sink_combined_configuration, char_height=4, char_width=4, line_width=text_width_mm - 28 , justification='R')
        l.endorigin()
        texts.pop(0)

    # Add each row of text to the label
    for i, text in enumerate(texts):
        y_position = y_positions[i]
        if i == 0:  # Row 1
            l.origin(0, y_position)
            l.write_text(text, char_height=5, char_width=5, line_width=text_width_mm, justification='C')
            l.endorigin()
        elif i == 1:  # Row 2 Column 1
            column1_width = (2 / 3) * text_width_mm  # Two-thirds of the row
            l.origin(x_positions_row2[0] + 2, y_position)
            l.write_text(text, char_height=4, char_width=4, line_width=column1_width, justification='L')
            l.endorigin()
        elif i == 2:  # Row 2 Column 2
            column1_width = (2 / 3) * text_width_mm
            column2_width = (1 / 3) * text_width_mm  # One-third of the row
            l.origin(x_positions_row2[0] + column1_width, y_position)
            l.write_text(text, char_height=4, char_width=4, line_width=column2_width, justification='R')
            l.endorigin()
        elif i == 3:  # Row 3 Column 1
            l.reverse_print(active='Y')
            l.origin(x_positions_row3_4[0], y_position - 0.8)  # Move the box 2 mm above row 3
            l.draw_box(width=text_width_mm * l.dpmm, height=5 * l.dpmm, thickness=20, color='B')  # Span the box all the way to the right
            l.endorigin()
            l.origin(x_positions_row3_4[0], y_position + 0.5)
            l.write_text(text, char_height=4, char_width=4, line_width=text_width_mm * l.dpmm, justification='L')
            l.endorigin()
        elif i == 4:  # Row 4 Column 1
            l.reverse_print(active='Y')
            l.origin(x_positions_row3_4[0], y_position - 0.8)  # Move the box 2 mm above row 4
            l.draw_box(width=text_width_mm * l.dpmm, height=5 * l.dpmm, thickness=20, color='B')  # Span the box all the way to the right
            l.endorigin()
            l.origin(x_positions_row3_4[0], y_position)
            l.write_text(text, char_height=4, char_width=4, line_width=text_width_mm * l.dpmm, justification='L')
            l.endorigin()
        elif i == 5:  # Row 3 and 4 Column 2
            l.origin(x_positions_row3_4[1], y_position)
            l.write_text(text, char_height=6, char_width=6, line_width=text_width_mm - 28, justification='R')
            l.endorigin()
            l.reverse_print(active='N')
        elif i == 6:  # Row 5
            l.origin(0, y_position)
            l.write_text(text, char_height=2.5, char_width=2.5, line_width=label_width_mm, justification='C') #add + 10 to label_width_mm if the text wraps occurs
            l.endorigin()

    # Add QR code
    folder_path = "Z:\\PUNCH\\SINKS\\Form Only"  # Hardcoded folder path
    qr_data = 'file:///' + folder_path.replace('\\', '/').replace(' ', '%20')  # Replace backslashes with forward slashes and encode spaces
    l.origin(76.2 + 2, 2)  # Adjust the position for QR code
    l.barcode('Q', qr_data, magnification=5)  # Adjust magnification as needed
    l.endorigin()

    zpl_command = l.dumpZPL()
    if total_labels > 25:
        zpl_command += "^XA^MMT^XZ"  # Set the print mode back to tear off, users will have to waste one label
    return zpl_command