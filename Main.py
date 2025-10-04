# ...existing code...
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
    def result_page():
        """Placeholder for the final design and visualization page."""
        with ui.column().classes('absolute-center items-center'):
            ui.label('Design Generation in Progress...').classes('text-4xl text-blue-400 font-bold')
            ui.spinner('dots', size='lg', color='blue')
            ui.button('Back to Parameters', on_click=lambda: ui.open('/parameters')).classes('mt-8')


# --- Run the App ---
if __name__ in {"__main__", "__mp_main__"}:
    # Register startup handlers (configure app and register routes)
    app.on_startup(configure_app)
    app.on_startup(define_routes)

    ui.run(title="Artemis Habitat Blueprint", reload=True)
# ...existing code...