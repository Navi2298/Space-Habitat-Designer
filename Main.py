from nicegui import ui
# We import the function that defines our Landing Page UI
from frontend.pages.page_1_landing import landing_page

# --- Page 1: Landing Page (Route: /) ---
@ui.page('/')
def index():
    """Defines the main route to run the landing page."""
    landing_page()

# --- Page 2: Parameters Page (Route: /parameters) ---
# This is required so the "Start Designing Now" button doesn't crash the app.
@ui.page('/parameters')
def params_placeholder():
    """Placeholder for the parameters page (Page 2)."""
    
    # Use the same dark background for continuity
    ui.add_head_html('<style>body { background-color: #04040A; }</style>')

    with ui.column().classes('absolute-center items-center p-10 bg-gray-900/90 backdrop-blur-sm rounded-3xl shadow-2xl max-w-xl border border-blue-700/50'):
        ui.label('Step 2: Parameters Page Coming Soon!').classes('text-3xl font-bold text-white mb-6')
        ui.label('The next page will collect mission details like crew size.').classes('text-lg text-gray-400 mb-6')
        ui.button('Go Back Home', on_click=lambda: ui.open('/')).classes('mt-4 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-full w-48 h-12')


if __name__ in {"__main__", "__mp_main__"}:
    # Set up the UI to run the web application
    ui.run(title="Habitat Designer", port=8080, reload=True)
