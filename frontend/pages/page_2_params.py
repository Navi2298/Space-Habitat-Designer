from nicegui import ui
from typing import Dict, Any

# Define a storage dictionary for the parameters.
# Using a dictionary for state management is clean and easy to pass around.
# NOTE: Mission Duration is stored as an integer (days) for calculations.
class Parameters:
    def __init__(self):
        # Initialize default parameters
        self.location: str = "Moon/Lunar Surface"
        self.crew_size: int = 4  # Changed default to 4 for better context
        self.mission_days: int = 30 # Store as integer
        self.mission_type: str = "Exploration"
        self.deployment_vehicle: str = "SLS"
        self.habitat_material: str = "Metallic"

# Global state object to store the parameters
current_parameters = Parameters()

def params_page() -> Parameters:
    """
    Creates the UI for setting habitat design parameters in a clean, professional card.
    Returns the live parameter object used for binding.
    """
    
    # Use a dark, stylized card for the input form
    with ui.card().classes('bg-gray-900 text-white shadow-xl max-w-lg mx-auto p-6 rounded-xl border border-blue-700'):
        
        # Header displaying the current state
        with ui.row().classes('w-full items-center justify-between mb-4'):
            ui.label('Design Mission Parameters').classes('text-2xl font-bold text-white')
            
            # Display current crew size and duration concisely
            with ui.row().classes('items-center'):
                ui.icon('group', size='sm').classes('text-blue-400')
                ui.label().bind_text_from(current_parameters, 'crew_size', backward=lambda x: f'{x} Crew').classes('text-lg text-blue-300 font-semibold mr-4')
                ui.icon('schedule', size='sm').classes('text-blue-400')
                ui.label().bind_text_from(current_parameters, 'mission_days', backward=lambda x: f'{x} Days').classes('text-lg text-blue-300 font-semibold')
        
        ui.separator().classes('w-full border-t border-blue-700/50 mb-6')

        # Two-column grid for inputs
        with ui.grid(columns=2).classes('w-full gap-y-6 gap-x-8'):
            
            # --- 1. Habitat Location (Select) ---
            ui.select(
                options=["Moon/Lunar Surface", "Transit (Deep Space, Cis-Lunar)", "Mars Transit/Surface"],
                label="Habitat Location",
            ).classes('w-full').props('dark filled').bind_value(current_parameters, 'location')

            # --- 2. Crew Members (Slider) ---
            with ui.column().classes('w-full'):
                ui.label('Crew Members (Min 2, Max 6)').classes('text-gray-400 text-sm')
                ui.slider(min=2, max=6, step=2).classes('w-full').props('dark').bind_value(current_parameters, 'crew_size')
            
            # --- 3. Mission Duration (Select: Integer values) ---
            mission_duration_options = {
                3: "3 Days (Short Stay)",
                30: "30 Days (Standard Rotation)",
                60: "60 Days",
                180: "180 Days (Long Duration)",
                1200: "1200+ Days (Mars Class)"
            }
            ui.select(
                options=mission_duration_options,
                label="Mission Duration (Days)",
            ).classes('w-full').props('dark filled').bind_value(current_parameters, 'mission_days')

            # --- 4. Mission Type (Select) ---
            ui.select(
                options=["Exploration", "Science & Research", "Technology Demonstration"],
                label="Mission Type",
            ).classes('w-full').props('dark filled').bind_value(current_parameters, 'mission_type')

            # --- 5. Deployment Vehicle (Select) ---
            ui.select(
                options=["SLS Block 1B Cargo", "Falcon Heavy", "Starship Cargo", "Commercial Launch Vehicle"],
                label="Deployment/Delivery Vehicle",
            ).classes('w-full').props('dark filled').bind_value(current_parameters, 'deployment_vehicle')

            # --- 6. Habitat Material (Select) ---
            ui.select(
                options=["Metallic Hard Shell", "Inflatable Softgoods", "Hybrid Structure", "In-Situ (3D Printed)"],
                label="Habitat Material/Structure",
            ).classes('w-full').props('dark filled').bind_value(current_parameters, 'habitat_material')

        # Action Button
        ui.button('Generate Initial Design', on_click=lambda: ui.open('/result')).classes('mt-8 w-full h-12 bg-blue-600 hover:bg-blue-500 text-lg font-bold shadow-lg shadow-blue-500/50 transition-transform transform hover:scale-[1.02] rounded-lg')
    
    # Returning the object makes it easy to access the data later
    return current_parameters

if __name__ in {"__main__", "__mp_main__"}:
    # Simple runner for testing the parameters page in isolation
    @ui.page('/parameters')
    def index():
        # Apply the star background style from the landing page
        ui.add_head_html("""
            <style>
                body { background-color: #04040A; }
                .star-field { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -10; }
                .star { position: absolute; background: #FFFFFF; border-radius: 50%; box-shadow: 0 0 5px 1px rgba(66, 165, 245, 0.5); animation-name: blink; animation-timing-function: linear; animation-iteration-count: infinite; }
                @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
            </style>
            <div id="star-field" class="star-field"></div>
            <script>
                // Simplified star script for standalone testing
                function createStar(size, duration) {
                    const star = document.createElement('div');
                    star.classList.add('star');
                    const x = Math.random() * 100;
                    const y = Math.random() * 100;
                    star.style.left = x + 'vw';
                    star.style.top = y + 'vh';
                    star.style.width = size + 'px';
                    star.style.height = size + 'px';
                    star.style.animationDuration = (duration + (Math.random() * 2)) + 's';
                    star.style.animationDelay = (Math.random() * 5) + 's';
                    return star;
                }
                const starField = document.getElementById('star-field');
                const numStars = 200; 
                for (let i = 0; i < numStars; i++) {
                    let size = (Math.random() * 3) + 1.0; 
                    let duration = 3 + (Math.random() * 4); 
                    starField.appendChild(createStar(size, duration));
                }
            </script>
        """)

        # Center the content container
        with ui.row().classes('w-screen h-screen items-center justify-center'):
            params_page()
            
    ui.run()
