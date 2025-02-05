import os
import asyncio
import subprocess
from nicegui import app

async def run_get_nomex_layers():
    """
    Pass the xml data to the exe to get the nomex layers but in the exe the arguments are swapped compared to the sink configuration exe
    # TODO: Fix the SENomexLayers.exe to accept the arguments in the same position as the sink configuration exe
    """
    file_path = app.storage.general.get('file_path', '')
    folder_path = os.path.dirname(file_path)
    table_data = app.storage.general.get('xml_table', [])

    if not folder_path or not table_data:
        print("Error: Missing folder path or table data!")
        return

    # Collect all unique codes from table data
    unique_codes = list({data.get('unique_code', '') for data in table_data if data.get('unique_code', '')})

    if unique_codes:
        exe_path = os.path.abspath('Packages/se_nomex_layers/SENomexLayers.exe')
        unique_codes_str = ','.join(unique_codes)
        print(f"Debug: Executing {exe_path} with folder path = {folder_path} and unique_codes = {unique_codes_str}")

        try:
            # Execute the EXE process
            process = await asyncio.create_subprocess_exec(
                exe_path, folder_path, unique_codes_str,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"Error running {exe_path}: {stderr.decode()}")
                return

            output = stdout.decode().strip()
            print(f"EXE Output:\n{output}")

        except Exception as e:
            print(f"Error while executing the process: {str(e)}")