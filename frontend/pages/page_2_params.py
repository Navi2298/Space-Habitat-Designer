from nicegui import ui

def params():
    """Creates the UI for setting habitat design parameters."""
    
    ui.label("Space Habitat Design Parameters").classes('text-h3')

    parameters = {
        "Habitat Location": "Moon/Lunar Surface",
        "Crew Members": 2,
        "Mission Duration": "3 days",
        "Mission Type": "Exploration",
        "Deployment Vehicle": "SLS",
        "Habitat Material": "Metallic"
    }

    # Habitat Location
    ui.select(
        ["Moon/Lunar Surface", "Transit (Deep Space, Cis-Lunar)", "Mars Transit Habitat"],
        label="Habitat Location",
        value=parameters["Habitat Location"],
        on_change=lambda e: parameters.update({"Habitat Location": e.value})
    )

    # Crew Members
    ui.slider(min=2, max=6, step=2, value=parameters["Crew Members"]).on_change(
        lambda e: parameters.update({"Crew Members": e.value})
    ).bind_value(parameters, 'Crew Members')


    # Mission Duration
    mission_duration_options = [3, 30, 60, 180, 1200]
    ui.select(
        options={duration: f"{duration} days" for duration in mission_duration_options},
        label="Mission Duration",
        value=3,
        on_change=lambda e: parameters.update({"Mission Duration": f"{e.value} days"})
    )

    # Mission Types
    ui.select(
        ["Exploration", "Science & Research"],
        label="Mission Type",
        value=parameters["Mission Type"],
        on_change=lambda e: parameters.update({"Mission Type": e.value})
    )

    # Deployment/Delivery Vehicles
    ui.select(
        ["SLS", "Commercial Launch Vehicles"],
        label="Deployment/Delivery Vehicle",
        value=parameters["Deployment Vehicle"],
        on_change=lambda e: parameters.update({"Deployment Vehicle": e.value})
    )

    # Habitat Material
    ui.select(
        ["Metallic", "Inflatable Softgoods", "Hybrid"],
        label="Habitat Material",
        value=parameters["Habitat Material"],
        on_change=lambda e: parameters.update({"Habitat Material": e.value})
    )

    # Display selected parameters
    ui.label("Selected Parameters:").classes('text-h5 mt-4')
    for key, value in parameters.items():
        ui.label(f"{key}:").bind_text_from(parameters, key, backward=lambda v, k=key: f"{k}: {v}")

    return parameters

if __name__ in {"__main__", "__mp_main__"}:
    @ui.page('/')
    def index():
        params()
    ui.run()