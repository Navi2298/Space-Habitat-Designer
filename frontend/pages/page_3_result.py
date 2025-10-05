from nicegui import ui
from visual_generation.generate_layout import generate_layout

def result_page(parameters):
    """
    Displays the generated habitat design based on the user's parameters.
    """
    layout_data = generate_layout(parameters)

    with ui.column().classes('w-full items-center p-8'):
        ui.label('Generated Habitat Design').classes('text-h3')

        with ui.card().classes('w-full max-w-4xl mt-4'):
            ui.image(layout_data['image_url']).classes('w-full')
            
            with ui.card_section():
                ui.label('Layout Description').classes('text-h6')
                ui.label(layout_data['description'])

                ui.label('Modules & Sizes').classes('text-h6 mt-4')
                for module_data in layout_data['modules']:
                    module_name = module_data['name']
                    size = layout_data['module_sizes'][module_name]
                    with ui.expansion(module_name, icon='widgets').classes('mb-2'):
                        ui.label(
                            f"Area: {size['area_m2']:.2f} m² | Volume: {size['volume_m3']:.2f} m³ | "
                            f"Dimensions: {size['width_m']:.2f}m x {size['depth_m']:.2f}m x {size['height_m']:.2f}m"
                        )

                ui.label('Floor Plan').classes('text-h6 mt-4')
                for layer in layout_data['floor_plan']:
                    ui.label(f"Layer {layer['layer']} (Radius: {layer['radius_m']:.2f} m)").classes('font-bold')
                    for mod in layer['modules']:
                        ui.label(
                            f"  {mod['module']} at {mod['angle_deg']:.1f}° | "
                            f"Distance from center: {mod['distance_from_center_m']:.2f} m"
                        )

        ui.button('Start Over', on_click=lambda: ui.navigate.to('/')).classes('mt-8')
