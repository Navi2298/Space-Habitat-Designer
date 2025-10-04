import os
from nicegui import ui, app
from typing import Callable

# --- Import Pages ---
from frontend.pages.page_1_landing import landing_page
from frontend.pages.page_2_params import params_page 

# --- Global Configuration ---

def configure_app():
    """Sets up global configuration and styling for NiceGUI."""
    
    # 1. Set up paths for static files (e.g., NASA logo)
    app.add_static_files('/Images', 'frontend/pages/Images') 
    
    # 2. Enable dark mode globally
    ui.dark_mode().enable()

def define_routes():
    """
    Defines all application routes using the NiceGUI ui.page decorator.
    This function is intended to be called during app startup.
    """
    
    # 1. Landing Page (Default Route)
    @ui.page('/')
    def index():
        """Renders the main landing page with the project overview."""
        landing_page()

    # 2. Parameters Input Page
    @ui.page('/parameters')
    def parameters_route():
        """
        Renders the page for defining habitat mission parameters.
        """
        # Center the content container using Tailwind classes
        with ui.row().classes('w-screen h-screen items-center justify-center'):
            # CALL the params_page with no arguments (matching its definition)
            params_page() 

    # 3. Placeholder Result Page
    @ui.page('/result')
    def result_page():
        """Placeholder for the final design and visualization page."""
        with ui.column().classes('absolute-center items-center'):
            ui.label('Design Generation in Progress...').classes('text-4xl text-blue-400 font-bold')
            ui.spinner('dots', size='lg', color='blue')
            ui.button('Back to Parameters', on_click=lambda: ui.open('/parameters')).classes('mt-8')


# --- Run the App ---
if __name__ in {"__main__", "__mp_main__"}:
    configure_app()
    
    # CRITICAL FIX: Use app.on_startup to register the routes,
    # which is the most reliable way to avoid the global scope RuntimeError.
    app.on_startup(define_routes) 
    
    ui.run(title="Artemis Habitat Blueprint", reload=True)
