import json
from jsonschema import validate, ValidationError
import os

def get_schema_path(schema_filename):
    """Constructs the absolute path to the schema file."""
    # Assumes this script is in visual_generation, goes up to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, 'schemas', schema_filename)

def load_schema(schema_path):
    """Loads a JSON schema from the given path."""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def validate_parameters(parameters):
    """
    Validates habitat parameters against the habitat_mapping_schema.json.

    Args:
        parameters (dict): A dictionary of parameters selected by the user.

    Returns:
        tuple[bool, str]: A tuple containing a boolean for success/failure
                         and a message string.
    """
    schema_path = get_schema_path('habitat_mapping_schema.json')
    schema = load_schema(schema_path)

    if schema is None:
        return False, f"Schema file not found at {schema_path}"

    try:
        # The schema expects the parameters to be nested under a "habitat" key
        instance_to_validate = {"habitat": parameters}
        validate(instance=instance_to_validate, schema=schema)
        return True, "Parameters are valid!"
    except ValidationError as e:
        # Create a more user-friendly error message
        if e.path:
            error_path = " -> ".join(map(str, e.path))
            return False, f"Validation Error for '{error_path}': {e.message}"
        else:
            return False, f"Validation Error: {e.message}"
    except Exception as e:
        return False, f"An unexpected error occurred during validation: {e}"


