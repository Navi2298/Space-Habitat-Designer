# frontend/three_d_viewer.py
from nicegui import ui

# We'll use a simple label to represent the 3D viewer for this example
# In a real app, this would be a ui.scene or other visualization tool.
scene = None 

def init_scene():
    """Initializes the 3D visualization area (Placeholder)."""
    global scene
    with ui.card().classes('w-full h-full p-4'):
        ui.label('3D SCENE AREA').classes('text-lg font-bold text-center')
        scene = ui.label('Current Modules: None').classes('text-gray-600')
    print("3D Scene initialized.")


def add_module_to_scene(module_name: str):
    """
    Function passed to the control panel to visually update the 3D scene.
    (Placeholder implementation)
    """
    global scene
    # This simulates updating the 3D view
    if scene:
        current_text = scene.text.replace("Current Modules: ", "")
        if current_text == 'None':
            scene.set_text(f"Current Modules: {module_name}")
        else:
            scene.set_text(f"Current Modules: {current_text}, {module_name}")
    print(f"Module '{module_name}' added to scene placeholder.")