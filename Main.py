# Main.py (Fixed)
from nicegui import ui
# Import core logic and UI components from our sub-folders
from backend.habitat_model import Habitat
from frontend.ui_panels import create_control_panel
from frontend.three_d_viewer import init_scene, add_module_to_scene


@ui.page('/')
def index():
    """
    Defines the overall application layout and initializes the core data model.
    """
    
    # 1. Define the Habitat model factory function
    def habitat_factory(crew_size, mission_days):
        return Habitat(crew_size=crew_size, mission_days=mission_days)

    # 2. Register and instantiate the refreshable component
    refreshable_wrapper = ui.refreshable(habitat_factory)
    
    # current_habitat_component is the NiceGUI wrapper for the object
    current_habitat_component = refreshable_wrapper(crew_size=4, mission_days=60)
    
    # ACCESSING THE HABITAT MODEL: Use the .content attribute once
    habitat_model = current_habitat_component.content

    # Header Section
    with ui.header().classes('bg-blue-800 text-white shadow-lg'):
        ui.label('Artemis Habitat Designer').classes('text-3xl font-extrabold')
        # Use the actual Habitat object's method
        ui.label(f'Crew: {habitat_model.get_crew_size()}').classes('text-xl ml-auto')

    # Main Content Layout
    with ui.row().classes('w-full p-4 gap-6 justify-center'):
        
        # Left Side: 3D Viewer
        with ui.card().classes('xl:w-3/5 lg:w-1/2 w-full min-h-[600px] shadow-2xl'):
            ui.label('3D Habitat Visualization').classes('text-xl font-semibold mb-2')
            init_scene() 
            
        # Right Side: Controls and Metrics Panel (Toolbox)
        with ui.card().classes('xl:w-1/4 lg:w-[45%] w-full shadow-2xl'):
            # PASS THE ACTUAL HABITAT MODEL and the scene function
            create_control_panel(habitat_model, add_module_to_scene) 


if __name__ in {"__main__", "__mp_main__"}:
    # Set up the UI to run the web application
    ui.run(title="Habitat Designer", port=8080, reload=True)