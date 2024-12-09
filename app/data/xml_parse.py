import xml.etree.ElementTree as ET
from tabulate import tabulate
from nicegui import app

def extract_nc_programs(func):
    async def wrapper (*args, **kwargs):
        xml_content = await func(*args, **kwargs)
        if xml_content is None:
            print("No XML content provided.")
            return []

        try:
            # Parse the XML content
            tree = ET.ElementTree(ET.fromstring(xml_content))
            root = tree.getroot()

            # Find the NcPrograms section
            nc_programs_section = root.find('NcPrograms')
            if nc_programs_section is None:
                print("No 'NcPrograms' section found in the XML file.")
                return []

            # Extract programs
            xml_data = []
            for i, program in enumerate(nc_programs_section.findall('NcProgram')):
                program_number = program.attrib.get('ProgramNo', "")
                total_no_of_runs = program.find('TotalNoOfRuns').text if program.find('TotalNoOfRuns') is not None else ""
                sheet = program.find('Sheet').text if program.find('Sheet') is not None else ""

                for part in program.findall('PartsInProgram/PartInProgram'):
                    quantity_on_sheet = int(part.find('QuantityOnSheet').text) if part.find('QuantityOnSheet') is not None else 0
                    part_number = part.attrib.get('PartoNo', "")

                    if '_' in part_number:
                        part_number = part_number.rsplit('_', 1)[0]

                    tops_part_number = part.find('TopsPartNo').text if part.find('TopsPartNo') is not None else ""
                    unique_code = part_number

                    # Store part details in xml_data for further processing
                    if 1 < quantity_on_sheet <= 4:
                        for j in range(1, quantity_on_sheet + 1):
                            x_of_y = f'{j} of {quantity_on_sheet}'
                            xml_data.append({
                                'program_number': program_number,
                                'total_number_of_runs': total_no_of_runs,
                                'sheet': sheet,
                                'part_number': part_number,
                                'tops_part_number': tops_part_number,
                                'quantity_on_sheet': quantity_on_sheet,
                                'unique_code': unique_code,
                                'x_of_y': x_of_y
                            })
                    else:
                        x_of_y = f'1 of {quantity_on_sheet}'
                        xml_data.append({
                            'program_number': program_number,
                            'total_number_of_runs': total_no_of_runs,
                            'sheet': sheet,
                            'part_number': part_number,
                            'tops_part_number': tops_part_number,
                            'quantity_on_sheet': quantity_on_sheet,
                            'unique_code': unique_code,
                            'x_of_y': x_of_y
                        })

            # Sort the xml_data using the custom_sort_key function
            xml_data.sort(key=custom_sort_key)

            header = xml_data[0].keys()
            rows = [x.values() for x in xml_data]
            # Print the xml_data as a formatted table
            print(tabulate(rows, header))

            # Enable JSON indentation for the storage
            app.storage.general.indent = True
            # Store the sorted data into app.storage.general
            app.storage.general['xml_table'] = xml_data

        except Exception as e:
            print(f"Error processing XML file: {e}")

    return wrapper

def custom_sort_key(row):
    program_number_parts = row['program_number'].rsplit('_', 1)
    program_base = program_number_parts[0]
    program_suffix = program_number_parts[1] if len(program_number_parts) == 2 else ""
    program_suffix_number = int(program_suffix) if program_suffix.isdigit() else float('inf')

    tops_part_number = row['tops_part_number']
    try:
        tops_number = int(tops_part_number) if tops_part_number.isdigit() else float('inf')
    except ValueError:
        tops_number = float('inf')

    return program_base, program_suffix_number, tops_number