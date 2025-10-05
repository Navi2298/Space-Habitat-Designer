import json
from jsonschema import validate, ValidationError
import random
import math

def generate_2d_visual(user_input):
    """
    Converts validated user input JSON into 2D visualization.
    - Top view layout
    - Sectional/floor views
    - Zones labeled
    """
    # Example placeholders:
    top_view = f"Top view for {user_input['name']}"
    sectional_views = [f"Floor {i+1}" for i in range(user_input.get("floors", 1))]

    # Return dict with visualization assets
    return {
        "top_view": top_view,
        "sectional_views": sectional_views
    }

def calculate_area_per_crew(mission_days, habitat_material):
    """Determine recommended area per crew based on mission duration and material."""
    if mission_days > 180:
        base_area = 25  # m² per crew (long duration)
    elif mission_days >= 30:
        base_area = 30  # m³ per crew (medium duration, using volume as proxy for area)
    else:
        base_area = 12  # m² per crew (short duration, minimum usable area)
    if "Inflatable" in habitat_material:
        base_area *= 1.2
    elif "Hybrid" in habitat_material:
        base_area *= 1.1
    elif "Regolith" in habitat_material:
        base_area *= 1.3
    return base_area

def module_dimensions(module_type):
    """Return minimum dimensions for each module type (width, depth, height in meters)."""
    dims = {
        "Private Quarters": (0.76, 0.76, 1.98),
        "Washroom/Hygiene": (1.14, 0.76, 1.98),
        "Waste Management (Human)": (1.02, 0.76, 1.98),
        "Waste Management (Trash)": (2.0, 1.0, 1.8),
        "Gym": (2.5, 2.5, 2.5),
        "Habitation": (3.0, 3.0, 2.5),
        "Laboratory": (2.5, 2.5, 2.5),
        "Airlock": (2.0, 2.0, 2.5),
        "Storage": (2.0, 2.0, 2.5),
        "Greenhouse": (2.5, 2.5, 2.5),
        "Medical Bay": (2.0, 2.0, 2.5),
    }
    return dims.get(module_type, (2.0, 2.0, 2.5))

def generate_floor_plan(modules, module_sizes, total_area, layers=1):
    """
    Iteratively arranges modules in a circular/radial floor plan.
    Returns a list of layers, each with its module arrangement and positions.
    """
    # Estimate radius needed for each layer
    layer_area = total_area / layers
    layer_radius = math.sqrt(layer_area / math.pi)
    floor_plan = []
    modules_per_layer = math.ceil(len(modules) / layers)
    module_idx = 0

    for layer in range(layers):
        layer_modules = modules[module_idx:module_idx+modules_per_layer]
        module_idx += modules_per_layer
        angle_step = 360 / max(1, len(layer_modules))
        positions = []
        for i, mod in enumerate(layer_modules):
            # Place modules evenly around the circle
            angle = i * angle_step
            mod_area = module_sizes[mod]["area_m2"]
            mod_radius = math.sqrt(mod_area / math.pi)
            positions.append({
                "module": mod,
                "angle_deg": angle,
                "distance_from_center_m": layer_radius - mod_radius,
                "size": module_sizes[mod]
            })
        floor_plan.append({
            "layer": layer + 1,
            "radius_m": layer_radius,
            "modules": positions
        })
    return floor_plan

def generate_layout(parameters):
    """
    Generates a conceptual habitat layout and a multi-layered floor plan.
    """
    crew_size = parameters.get('crew_size', 4)
    mission_days = parameters.get('mission_days', 30)
    habitat_material = parameters.get('habitat_material', 'Metallic Hard Shell')
    location = parameters.get('location', 'Unknown')
    mission_type = parameters.get('mission_type', 'Exploration')

    area_per_crew = calculate_area_per_crew(mission_days, habitat_material)
    total_area = area_per_crew * crew_size

    # Required modules
    modules = [
        "Private Quarters",
        "Washroom/Hygiene",
        "Waste Management (Human)",
        "Waste Management (Trash)",
        "Gym",
        "Habitation",
        "Storage"
    ]
    if mission_type == "Science & Research":
        modules.append("Laboratory")
    if mission_type == "Exploration":
        modules.append("Airlock")
    if mission_days > 180:
        modules.append("Greenhouse")
    if crew_size > 4:
        modules.append("Medical Bay")

    # Calculate module sizes
    module_sizes = {}
    for module in modules:
        w, d, h = module_dimensions(module)
        area = round(w * d, 2)
        volume = round(w * d * h, 2)
        module_sizes[module] = {
            "width_m": w,
            "depth_m": d,
            "height_m": h,
            "area_m2": area,
            "volume_m3": volume
        }

    # Distribute total area among modules (main Habitation gets largest share)
    main_hab_area = round(total_area * 0.35, 2)
    if "Habitation" in module_sizes:
        module_sizes["Habitation"]["area_m2"] = main_hab_area

    # Determine number of layers/floors
    layers = 1
    if crew_size > 4 or mission_days > 180:
        layers = 2

    # Generate floor plan
    floor_plan = generate_floor_plan(modules, module_sizes, total_area, layers)

    layout_description = (
        f"{habitat_material} habitat for {crew_size} crew on a {mission_days}-day {location} mission.\n"
        f"Total recommended area: {total_area:.1f} m² ({area_per_crew:.1f} m² per crew).\n"
        f"Modules included: {', '.join(modules)}.\n"
        f"Main habitation module area: {main_hab_area} m².\n"
        f"Arranged in {layers} layer(s) with radial/circular layout."
    )

    return {
        "modules": modules,
        "module_sizes": module_sizes,
        "description": layout_description,
        "floor_plan": floor_plan,
        "image_url": f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/600"
    }
