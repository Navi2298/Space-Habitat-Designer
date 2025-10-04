# frontend/ui_panels.py
from nicegui import ui
from backend.habitat_model import Habitat

def create_control_panel(habitat_model: Habitat, add_module_callback):
    """
    Creates the habitat control and metrics panel.

    Args:
        habitat_model: The instance of the Habitat class.
        add_module_callback: A function (from three_d_viewer.py) to update the scene.
    """
    
    ui.label('Habitat Controls').classes('text-2xl font-bold mb-4')
    
    # --- Metrics ---
    with ui.column().classes('p-2 border rounded-lg bg-gray-100 mb-4 w-full'):
        ui.label(f'Mission Days: {habitat_model._mission_days}')
        
        # Use a refreshable label to track the number of modules
        @ui.refreshable
        def module_count_label():
            ui.label(f'Total Modules: {len(habitat_model.modules)}').classes('font-semibold')

        module_count_label() # Initial call
        
    # --- Module Addition ---
    ui.label('Add Modules').classes('text-xl font-semibold mt-4')
    
    module_input = ui.input(label='Module Name', value='Living_Quarters').classes('w-full')
    
    def handle_add_module():
        """Handles the button click to add a new module."""
        name = module_input.value
        
        # 1. Update the core data model
        habitat_model.add_module(name)
        
        # 2. Update the UI metrics
        module_count_label.refresh()
        
        # 3. Update the 3D scene visualization
        add_module_callback(name)
        
        ui.notify(f'Added {name}', type='positive')
        
    ui.button('Add Module', on_click=handle_add_module).classes('mt-2 w-full')