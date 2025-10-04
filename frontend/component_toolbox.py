from nicegui import ui
from .three_d_viewer import add_module_to_scene

# Define the standard components available to the user
HABITAT_COMPONENTS = {
    'Sleeping Pod': {
        'color': '#00FFFF', # Cyan
        'geometry': 'new THREE.BoxGeometry(0.7, 0.7, 1)',
        'description': 'Individual crew sleeping and resting area.',
        'mass_kg': 50, # Example mass
        'volume_m3': 0.49
    },
    'Work/Lab Area': {
        'color': '#FFFF00', # Yellow
        'geometry': 'new THREE.BoxGeometry(1.5, 1.5, 0.2)',
        'description': 'Primary area for research and operations.',
        'mass_kg': 150,
        'volume_m3': 0.45
    },
    'Airlock Module': {
        'color': '#FF0000', # Red
        'geometry': 'new THREE.CylinderGeometry(0.5, 0.5, 0.5, 16)',
        'description': 'Sealed entry/exit point for EVAs.',
        'mass_kg': 200,
        'volume_m3': 0.39
    },
    'Gym Area': {
        'color': '#FF00FF', # Magenta
        'geometry': 'new THREE.TorusGeometry(0.8, 0.1, 16, 100)',
        'description': 'Exercise equipment and fitness space.',
        'mass_kg': 100,
        'volume_m3': 0.2
    },
    'ECLSS (Life Support)': {
        'color': '#00FF00', # Green
        'geometry': 'new THREE.BoxGeometry(1, 1, 1)',
        'description': 'Environmental control and life support systems.',
        'mass_kg': 300,
        'volume_m3': 1.0
    },
}

def create_toolbox():
    """
    Creates the NiceGUI interface for the Component Library.
    """
    with ui.column().classes('p-4 space-y-3 w-full'):
        ui.label('Habitat Component Library').classes('text-xl font-extrabold text-white bg-gray-800 p-2 rounded-lg shadow-lg')
        
        for name, data in HABITAT_COMPONENTS.items():
            
            # The function that runs when the button is clicked
            def spawn_module(module_name=name, color=data['color'], geometry=data['geometry']):
                add_module_to_scene(module_name, color, geometry)
                ui.notify(f"Spawned {module_name}. Click it in 3D viewer to drag.", type='info')

            with ui.card().classes('w-full p-2 hover:shadow-2xl transition duration-200 border-l-4 border-l-sky-400'):
                ui.label(name).classes('font-bold text-lg')
                ui.label(data['description']).classes('text-sm text-gray-500')
                ui.button(
                    f'Add {name}',
                    on_click=spawn_module
                ).classes('w-full mt-2 bg-sky-600 hover:bg-sky-700')
