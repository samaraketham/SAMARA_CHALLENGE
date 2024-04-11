import json
from datetime import datetime

def sanitize_key(key):
    return key.strip()

def transform_value(value, data_type):
    if data_type == 'S':
        # Transform RFC3339 formatted Strings to Unix Epoch
        try:
            return int(datetime.fromisoformat(value).timestamp())
        except ValueError:
            return value.strip()
    elif data_type == 'N':
        # Strip leading zeros
        return int(value)
    elif data_type == 'BOOL':
        # Transform truthy/falsy values to Boolean
        return value.lower() in ['1', 't', 'true']
    elif data_type == 'NULL':
        # Transform 1, t, T, TRUE, true to True, omit otherwise
        return None if value.lower() in ['1', 't', 'true'] else None
    else:
        # Unsupported data type
        return None

def transform_json(input_json):
    transformed_data = {}
    for key, value in input_json.items():
        # Skip empty keys
        if not key.strip():
            continue
        
        # Sanitize key
        key = sanitize_key(key)

        # Parse data type and value
        data_type, value = next(iter(value.items()))

        # Transform value based on data type
        transformed_value = transform_value(value, data_type)

        # Add transformed key-value pair to result
        if transformed_value is not None:
            transformed_data[key] = transformed_value

    return transformed_data

def main():
    with open('input.json', 'r') as file:
        input_json = json.load(file)

    transformed_data = transform_json(input_json)

    # Create output JSON
    output_json = [transformed_data]

    # Output to stdout
    print(json.dumps(output_json, indent=2))

if __name__ == '__main__':
    main()
