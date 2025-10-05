from nicegui import ui
from visual_generation.generate_layout import generate_layout

def result_page(parameters):
    """
    Displays the generated habitat design based on the user's parameters.
    """
    
    # Generate the layout using the validated parameters
    layout_data = generate_layout(parameters)

    with ui.column().classes('w-full items-center p-8'):
        ui.label('Generated Habitat Design').classes('text-h3')

        with ui.card().classes('w-full max-w-4xl mt-4'):
            ui.image(layout_data['image_url']).classes('w-full')
            
            with ui.card_section():
                ui.label('Layout Description').classes('text-h6')
                ui.label(layout_data['description'])

                ui.label('Modules').classes('text-h6 mt-4')
                for module in layout_data['modules']:
                    ui.chip(module, color='blue')

        ui.button('Start Over', on_click=lambda: ui.navigate.to('/')).classes('mt-8')
