import os
import json
import csv

# Step 1: Function to find all JSON files in the 'data' directory
def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

# Step 2: Function to flatten JSON structures
def flatten_json(nested_json, parent_key='', sep='_'):
    """Flatten JSON data with nested structures."""
    items = {}
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_json(value, new_key, sep=sep))
        elif isinstance(value, list):
            if len(value) == 2 and isinstance(value[0], (float, int)) and isinstance(value[1], (float, int)):
                # Special handling for coordinate-like lists
                items[new_key + '_lat'] = value[1]
                items[new_key + '_lon'] = value[0]
            else:
                items[new_key] = str(value)  # Convert list to string
        else:
            items[new_key] = value
    return items

# Step 3: Function to read JSON files, flatten them, and write to CSV
def json_to_csv(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Flatten the JSON data
    flat_data = flatten_json(data)

    # Prepare CSV filename (replace .json with .csv)
    csv_file = json_file.replace('.json', '.csv')

    # Write to CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=flat_data.keys())
        writer.writeheader()
        writer.writerow(flat_data)

    print(f"Converted {json_file} to {csv_file}")

# Main function to find all JSON files and convert them to CSV
def main():
    data_directory = './data'  # Path to the 'data' directory
    json_files = find_json_files(data_directory)

    for json_file in json_files:
        json_to_csv(json_file)

if __name__ == "__main__":
    main()