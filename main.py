"""
This module initializes the NiceGUI application and handles startup and shutdown events.
"""
from nicegui import ui, app
from app.startup import startup

try:
    import pyi_splash # type: ignore
except ImportError:
    pyi_splash = None

app.on_startup(startup)

@app.on_startup
def close_splash():
    """
    Close splash screen after the startup function is called
    """
    if pyi_splash and pyi_splash.is_alive():
        pyi_splash.close()

@app.on_shutdown
def shutdown():
    """
    Shutdown the server when the app is closed
    """
    print("Shutting down the server...")
    app.shutdown()

ui.run(native=True, reload=False, port=5000, title="Label Printer", favicon="🏷️")
