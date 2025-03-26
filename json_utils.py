
# def extract_values(data, key):
#     # Check if the key is directly available (like "bgp_asn")
#     if key in data:
#         return data[key]
    
#     # If the key is inside a list of dictionaries (like "vms")
#     for outer_key in data:
#         if isinstance(data[outer_key], list):  # Check if the value is a list
#             values = []
#             for item in data[outer_key]:
#                 if isinstance(item, dict) and key in item:
#                     values.append(item[key])  # Append the value of the key
#             if values:
#                 return values
    
#     # If key isn't found, return a message
#     return f"Key '{key}' not found in the data."
import json
import os

def load_json_file(file_path):
    """
    Load a JSON file and return its data as a Python dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ JSON file '{file_path}' not found.")
    
    with open(file_path, 'r') as json_file:
        try:
            data = json.load(json_file)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Failed to parse JSON file '{file_path}': {e}")

def extract_values(data, key):
    """
    Extract values associated with a given key from a JSON-like dictionary.
    """
    # Check if the key is directly available (like "bgp_asn")
    if key in data:
        return data[key]
    
    # If the key is inside a list of dictionaries (like "vms")
    for outer_key in data:
        if isinstance(data[outer_key], list):  # Check if the value is a list
            values = []
            for item in data[outer_key]:
                if isinstance(item, dict) and key in item:
                    values.append(item[key])  # Append the value of the key
            if values:
                return values

    return f"Key '{key}' not found in the data."
        