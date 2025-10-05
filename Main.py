import os
from nicegui import ui, app

# --- Global Configuration (no UI creation at import) ---
def configure_app():
    """Sets up global configuration and styling for NiceGUI at startup."""
    # 1. Set up paths for static files (e.g., NASA logo)
    app.add_static_files('/Images', 'frontend/pages/Images')
    # 2. Enable dark mode (executed on startup, not at import)
    ui.dark_mode().enable()

def define_routes():
    """
    Register application routes. Imports pages here to avoid importing
    modules that create UI at import time.
    """
    # Import pages inside the startup handler to avoid global UI creation
    from frontend.pages.page_1_landing import landing_page
    from frontend.pages.page_2_params import params_page
    from frontend.pages.page_3_result import result_page  # Import the result page

    @ui.page('/')
    def index():
        """Renders the main landing page with the project overview."""
        landing_page()

    @ui.page('/parameters')
    def parameters_route():
        """Renders the page for defining habitat mission parameters."""
        with ui.row().classes('w-screen h-screen items-center justify-center'):
            params_page()

    @ui.page('/result')
    def result_page_route():
        """Renders the final design and visualization page."""
        parameters = app.storage.user.get('parameters')  # Retrieve parameters from session
        if parameters:
            result_page(parameters)  # Pass parameters to result_page
        else:
            ui.label("Error: No parameters found. Please go back and enter them.").classes('text-red-500')


# --- Run the App ---
if __name__ in {"__main__", "__mp_main__"}:
    # Register startup handlers (configure app and register routes)
    app.on_startup(configure_app)
    app.on_startup(define_routes)

    # Add a storage_secret for user storage
    storage_secret = os.urandom(32).hex()
    ui.run(title="Artemis Habitat Blueprint", reload=True, storage_secret=storage_secret)