import json
import subprocess
import sys
import os
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
    Calls the C++ backend executable to generate the habitat layout.
    It passes parameters via stdin and receives results via stdout.
    """
    try:
        # Determine the path to the C++ executable
        # Assumes this script is in 'visual_generation' and the executable is in 'cpp_backend'
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        executable_name = "habitat_optimizer.exe"
        # Correctly locate the executable in the build directory
        executable_path = os.path.join(project_root, "cpp_backend", "build", "Release", executable_name)

        if not os.path.exists(executable_path):
            # Fallback for Debug builds
            executable_path_debug = os.path.join(project_root, "cpp_backend", "build", "Debug", executable_name)
            if os.path.exists(executable_path_debug):
                executable_path = executable_path_debug
            else:
                return {
                    "status": "error",
                    "description": f"Backend executable not found in Release or Debug build directories. Looked for: {executable_path}",
                    "modules": []
                }

        # The C++ backend expects the parameters to be nested under a "habitat" key
        input_data = {"habitat": parameters}
        input_json = json.dumps(input_data)

        # Run the C++ process
        process = subprocess.run(
            [executable_path],
            input=input_json,
            capture_output=True,
            text=True,
            check=True, # Throws an exception if the process returns a non-zero exit code
            encoding='utf-8'
        )

        # Parse the JSON output from the C++ process
        return json.loads(process.stdout)

    except subprocess.CalledProcessError as e:
        # If the C++ process returns an error, capture its stderr
        return {
            "status": "error",
            "description": f"The C++ backend failed with an error:\n{e.stderr}",
            "image_url": "",
            "modules": []
        }
    except json.JSONDecodeError:
        return {
            "status": "error",
            "description": "Failed to parse the JSON output from the C++ backend.",
            "image_url": "",
            "modules": []
        }
    except Exception as e:
        return {
            "status": "error",
            "description": f"An unexpected error occurred while running the backend: {str(e)}",
            "image_url": "",
            "modules": []
        }
