from nicegui import ui
# We import the function that defines our Landing Page UI
from frontend.pages.page_1_landing import landing_page
from frontend.pages.page_2_params import params

@ui.page('/')
def index_page():
    landing_page()

@ui.page('/parameters')
def parameters_page():
    params()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Habitat Designer", port=8080, reload=True, show=True)
