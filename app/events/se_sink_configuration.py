import asyncio
import os.path
import subprocess
from nicegui import app

async def run_sink_configuration():
    file_path = app.storage.general.get('file_path', '')
    dxf_file_path = app.storage.general.get('dxf_file_path', '')
    table_data = app.storage.general.get('xml_table', [])

    # Determine which path to use
    if "0-BOOST NC\\PR\\PINK-RUSH" in file_path and dxf_file_path:
        # Use DXF path but remove the file name
        folder_path = os.path.dirname(dxf_file_path)
    else:
        folder_path = os.path.dirname(file_path)

    if not folder_path or not table_data:
        print("Error: Missing folder path or table data!")
        return

    # Collect all unique codes from table data
    unique_codes = list({data.get('unique_code', '') for data in table_data if data.get('unique_code', '')})

    if unique_codes:
        exe_path = os.path.abspath('Packages/se_sink_configuration/SE Sink Configuration.exe')
        unique_codes_str = ','.join(unique_codes)
        print(f"Debug: Executing {exe_path} with unique_codes = {unique_codes_str} and folder path = {folder_path}")

        try:
            # Execute the EXE process
            process = await asyncio.create_subprocess_exec(
                exe_path, unique_codes_str, folder_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"Error running {exe_path}: {stderr.decode()}")
                return

            output = stdout.decode().strip()

            # Parse the EXE output
            sink_combined_configurations = {}
            current_part = ""
            sink_config = {
                "sink_configuration": "",
                "sinkl": "",
                "sinkw": "",
                "sinkh": "",
                "sink_drain": "",
                "sink_drain_location": ""
            }

            for line in output.splitlines():
                line = line.strip()

                if line.startswith("Part:"):
                    # Save the last part's configuration
                    if current_part and all(sink_config.values()):
                        sink_combined_configuration = (
                            f"{sink_config['sink_configuration']}_"
                            f"{sink_config['sink_drain']}{sink_config['sink_drain_location']}_"
                            f"{sink_config['sinkl']}{sink_config['sinkw']}{sink_config['sinkh']}"
                        )
                        sink_combined_configurations[current_part] = sink_combined_configuration

                    # Initialize a new part
                    current_part = line.split(":")[1].strip()
                    sink_config = {key: "" for key in sink_config}  # Reset values

                elif line.startswith("SINK CONFIGURATION:"):
                    sink_config['sink_configuration'] = line.split(":")[1].strip()
                elif line.startswith("SINKL:"):
                    sink_config['sinkl'] = line.split(":")[1].strip()
                elif line.startswith("SINKW:"):
                    sink_config['sinkw'] = line.split(":")[1].strip()
                elif line.startswith("SINKH:"):
                    sink_config['sinkh'] = line.split(":")[1].strip()
                elif line.startswith("SINK DRAIN:"):
                    sink_config['sink_drain'] = line.split(":")[1].strip()
                elif line.startswith("SINK DRAIN LOCATION:"):
                    sink_config['sink_drain_location'] = line.split(":")[1].strip()

            # Save the last part's configuration
            if current_part and all(sink_config.values()):
                sink_combined_configuration = (
                    f"{sink_config['sink_configuration']}_"
                    f"{sink_config['sink_drain']}{sink_config['sink_drain_location']}_"
                    f"{sink_config['sinkl']}{sink_config['sinkw']}{sink_config['sinkh']}"
                )
                sink_combined_configurations[current_part] = sink_combined_configuration

            print(f"Debug: sink_combined_configurations = {sink_combined_configurations}")  # Debugging

            # Log VB Script output
            print(f"VB Script Output:\n{output}")

            # Update table_data with the sink_combined_configurations
            for data in table_data:
                unique_code = data.get('unique_code', '')
                if unique_code and unique_code in sink_combined_configurations:
                    data['sink_combined_configuration'] = sink_combined_configurations[unique_code]
                    print(f"EXE Output for {unique_code}: {sink_combined_configurations[unique_code]}")  # Log config

        except Exception as e:
            print(f"Error while executing the process: {str(e)}")