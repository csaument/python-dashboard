import json

def clean_data(file_path):
    # Load JSON data from file
    with open(file_path, "r") as f:
        data = json.load(f)
        print(f"{file_path}: {len(data)}")

    # Create a list to store unique values
    unique_data = []

    # Loop through the list of JSON objects, and add each object to the unique list only if it doesn't exist in the unique list
    for d in data:
        if d not in unique_data:
            unique_data.append(d)

    # Write the unique list back to the file
    with open(file_path, "w") as f:
        json.dump(unique_data, f)

    print(f"Cleaned {file_path}: {len(unique_data)}")

# Clean the data in both files
house_file = "./Data/house_members.json"
senate_file = "./Data/senate_members.json"
clean_data(house_file)
clean_data(senate_file)