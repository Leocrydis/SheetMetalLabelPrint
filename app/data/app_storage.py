import json
from nicegui import app

def save_data(key, data):
    keys = key.split('.')
    d = app.storage.general
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = data
    # Optionally, save the updated data back to the JSON file
    with open('.nicegui/storage-general.json', 'w') as file:
        json.dump(app.storage.general, file, indent=4)