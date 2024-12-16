import zpl
from nicegui import app
import os

def create_label(data, data_type, total_labels):
    # Convert inches to millimeters (1 inch = 25.4 mm)
    label_width_mm = 4 * 25.4  # 4 inches wide
    label_height_mm = 1 * 25.4  # 1 inch tall

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

    # Add the sink_combined_configuration to the left of row 1 if available
    sink_combined_configurations = data.get('sink_combined_configuration', '')
    if sink_combined_configurations:
        texts.insert(0, sink_combined_configurations)

    # Define the y positions for each row (in millimeters)
    y_positions = [2, 7, 7, 13, 18, 13, 23]  # Adjust these values as needed

    # Define the x positions for each column in row 2 (in millimeters)
    x_positions_row2 = [0, label_width_mm - (label_width_mm / 2) - 4]  # Column 1 starts at 0, Column 2 is offset by 4 mm from the right edge

    # Define the x positions for each column in rows 3 and 4 (in millimeters)
    x_positions_row3_4 = [0, 26]  # Column 1 starts at 0, Column 2 starts at 26 mm

    # Add the sink_combined_configuration to the left of row 1 if available
    sink_combined_configuration = data.get('sink_combined_configuration', '')
    if sink_combined_configuration:
        l.origin(5, y_positions[0])
        l.write_text(sink_combined_configuration, char_height=3, char_width=3, line_width=label_width_mm / 2, justification='L')
        l.endorigin()
        texts.pop(0)

    # Add each row of text to the label
    for i, text in enumerate(texts):
        y_position = y_positions[i]
        if i == 0:  # Row 1
            l.origin(0, y_position)
            l.write_text(text, char_height=5, char_width=5, line_width=label_width_mm, justification='C')
            l.endorigin()
        elif i == 1:  # Row 2 Column 1
            l.origin(x_positions_row2[0] + 2, y_position)
            l.write_text(text, char_height=4, char_width=4, line_width=(label_width_mm * 2 / 3), justification='L')
            l.endorigin()
        elif i == 2:  # Row 2 Column 2
            l.origin(x_positions_row2[0] + (label_width_mm * 2 / 3), y_position)
            l.write_text(text, char_height=4, char_width=4, line_width=(label_width_mm / 3), justification='C')
            l.endorigin()
        elif i == 3:  # Row 3 Column 1
            l.reverse_print(active='Y')
            l.origin(x_positions_row3_4[0], y_position - 0.8)  # Move the box 2 mm above row 3
            l.draw_box(width=label_width_mm * l.dpmm, height=5 * l.dpmm, thickness=20, color='B')  # Span the box all the way to the right
            l.endorigin()
            l.origin(x_positions_row3_4[0] + 2, y_position + 0.5)
            l.write_text(text, char_height=4, char_width=4, line_width=label_width_mm * l.dpmm, justification='L')
            l.endorigin()
        elif i == 4:  # Row 4 Column 1
            l.reverse_print(active='Y')
            l.origin(x_positions_row3_4[0], y_position - 0.8)  # Move the box 2 mm above row 4
            l.draw_box(width=label_width_mm * l.dpmm, height=5 * l.dpmm, thickness=20, color='B')  # Span the box all the way to the right
            l.endorigin()
            l.origin(x_positions_row3_4[0] + 3, y_position)
            l.write_text(text, char_height=4, char_width=4, line_width=label_width_mm * l.dpmm, justification='L')
            l.endorigin()
        elif i == 5:  # Row 3 and 4 Column 2
            l.origin(x_positions_row3_4[1], y_position + 1)
            l.write_text(text, char_height=8, char_width=8, line_width=label_width_mm - 28, justification='C')
            l.endorigin()
            l.reverse_print(active='N')
        elif i == 6:  # Row 5
            l.origin(0, y_position)
            l.write_text(text, char_height=2.5, char_width=2.5, line_width= 4 * 25.4 , justification='C') #add + 10 to label_width_mm if the text wraps occurs
            l.endorigin()

    zpl_command = l.dumpZPL()
    if total_labels > 25:
        zpl_command += "^XA^MMT^XZ"  # Set the print mode back to tear off, users will have to waste one label
    return zpl_command

def create_lst_label():
    # Convert inches to millimeters (1 inch = 25.4 mm)
    label_width_mm = 4 * 25.4  # 4 inches wide
    label_height_mm = 1 * 25.4  # 1 inch tall

    # Create a new label with dimensions in millimeters
    l = zpl.Label(label_height_mm, label_width_mm)

    # Determine the .lst file path based on the XML file path in file_breakdown
    file_breakdown = app.storage.general.get('file_breakdown', {})
    xml_file_path = file_breakdown.get('file_path', 'default.xml').replace('\\', '/')
    lst_file_name = os.path.splitext(os.path.basename(xml_file_path))[0] + '.lst'
    lst_file_path = os.path.join(os.path.dirname(xml_file_path), lst_file_name).replace('\\', '/')

    # Split the text into multiple lines if it exceeds the label width
    max_line_length = int(label_width_mm / 2.5)  # Adjust this value as needed
    lines = []
    current_line = ""
    for word in lst_file_path.split('/'):
        if len(current_line) + len(word) + 1 <= max_line_length:
            current_line += "/" + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if (current_line):
        lines.append(current_line)

    # Add the .lst file path to the label, centered
    for i, line in enumerate(lines):
        y_position = (label_height_mm / 2) - (len(lines) - 1 - i) * 5  # Adjust the Y position for each line
        x_postion = (label_width_mm / 2) - (len(line) * 2.5) / 2
        l.origin(x_postion + 6, y_position)
        l.write_text(line, char_height=5, char_width=5)
        l.endorigin()
    zpl_command = l.dumpZPL()
    print(zpl_command)

    return l.dumpZPL()

def check_lst_file_exists():
    file_breakdown = app.storage.general.get('file_breakdown', {})
    xml_file_path = file_breakdown.get('file_path', 'default.xml').replace('\\', '/')
    lst_file_name = os.path.splitext(os.path.basename(xml_file_path))[0] + '.lst'
    lst_file_path = os.path.join(os.path.dirname(xml_file_path), lst_file_name).replace('\\', '/')
    return os.path.exists(lst_file_path)