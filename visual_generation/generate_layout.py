import json
from jsonschema import validate, ValidationError

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
