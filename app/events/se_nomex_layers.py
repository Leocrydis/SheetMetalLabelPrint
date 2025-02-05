import asyncio
import os.path
import subprocess
from nicegui import app

async def run_get_nomex_layers():
    file_path = app.storage.general.get('file_path', '')
    folder_path = os.path.dirname(file_path)
    table_data = app.storage.general.get('xml_table', [])
