import json
from jsonschema import validate, ValidationError

def load_schema(schema_path='schemas/habitat_mapping_schema.json'):
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    return schema

def validate_input(user_input, schema):
    try:
        validate(instance=user_input, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)

