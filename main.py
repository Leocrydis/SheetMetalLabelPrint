from nicegui import ui, app
from app.startup import startup

try:
    import pyi_splash
except ImportError:
    pyi_splash = None

app.on_startup(startup)

# Close the splash screen after the startup function is called
@app.on_startup
def close_splash():
    if pyi_splash and pyi_splash.is_alive():
        pyi_splash.close()

#When the app is closed shut down server, this is for when the app is native mode with no console to close the application
@app.on_shutdown
def shutdown():
    print("Shutting down the server...")
    app.shutdown()

ui.run(native=True, reload=False, port=5000, title="Label Printer", favicon="🏷️")
