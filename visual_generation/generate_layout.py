import json
from jsonschema import validate, ValidationError
import random

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

def generate_layout(parameters):
    """
    Generates a conceptual habitat layout based on user-defined parameters.

    This is a placeholder function that returns a mock layout. In a real
    application, this would involve complex geometric calculations.

    Args:
        parameters (dict): A dictionary of validated user parameters.

    Returns:
        dict: A dictionary containing the generated layout details.
    """
    
    # Determine the number of modules based on crew size and mission duration
    crew_size = parameters.get('crew_size', 4)
    mission_days = parameters.get('mission_days', 30)
    
    num_modules = 2 + (crew_size // 2) + (mission_days // 90)
    
    # Define potential module types
    module_types = [
        "Habitation", "Laboratory", "Airlock", "Storage", 
        "Greenhouse", "Sanitation", "Medical Bay", "Gym"
    ]
    
    # Generate a list of modules for the habitat
    generated_modules = random.sample(module_types, k=min(num_modules, len(module_types)))
    if "Habitation" not in generated_modules:
        generated_modules[0] = "Habitation" # Ensure there's always a place to live

    # Generate a simple textual description of the layout
    layout_description = f"A {parameters.get('habitat_material', 'metallic')} habitat designed for a crew of {crew_size} on a {mission_days}-day mission. "
    layout_description += f"It is located at: {parameters.get('location', 'Unknown')}. "
    layout_description += "The layout consists of a linear arrangement of the following modules: "
    layout_description += ", ".join(generated_modules) + "."

    return {
        "modules": generated_modules,
        "description": layout_description,
        "image_url": f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/600" # Placeholder image
    }
