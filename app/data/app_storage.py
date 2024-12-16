import json
import os
from nicegui import app

def initialize_storage():
    app.storage.general.update({
        "xml_table": [],
        "file_path": "",
        "csv_table": [],
        "file_breakdown": {
            "file_path": "",
            "customer_location": "",
            "job_name": "",
            "item_name": ""
        },
        "dxf_file_path": "",
        "form_only_sinks": [],
        "matched_sinks": [],
        "unmatched_sinks": [],
        "missing_programs": {
            "list": [],
            "count": 0
        }
    })

def save_data(key, data):
    keys = key.split('.')
    d = app.storage.general
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = data
    # Optionally, save the updated data back to the JSON file
    with open('.nicegui/storage-general.json', 'w') as file:
        json.dump(app.storage.general, file, indent=4)

def load_data():
    try:
        with open('.nicegui/storage-general.json', 'r') as file:
            app.storage.general.update(json.load(file))
    except FileNotFoundError:
        initialize_storage()
    except json.JSONDecodeError:
        initialize_storage()

def load_data_key(key):
    return app.storage.general.get(key)

# Load the JSON data if the file exists, otherwise initialize with default values
if os.path.exists('.nicegui/storage-general.json'):
    with open('.nicegui/storage-general.json', 'r') as file:
        data = json.load(file)
else:
    data = {
         "xml_table": [],
        "file_path": "",
        "csv_table": [],
        "file_breakdown": {
            "file_path": "",
            "customer_location": "",
            "job_name": "",
            "item_name": ""
        },
        "dxf_file_path": "",
        "form_only_sinks": [],
        "matched_sinks": [],
        "unmatched_sinks": [],
        "missing_programs": {
            "list": [],
            "count": 0
        }
    }
    app.storage.general.update(data)