import json

with open('color.json', 'r') as f:
    data = json.load(f)

# Initialize an array to store the formatted data
COLOR_CATEGORIES = []

# Iterate over each item in the JSON file
for key, value in data.items():
    # Extract relevant information
    name = key
    color = f"rgb({value['rgb'][0]}, {value['rgb'][1]}, {value['rgb'][2]})"


    # Create a dictionary for the item
    item = {
        'name': name,
        'color': color
    }

    # Append the item to the array
    COLOR_CATEGORIES.append(item)

# Print the formatted array
print(COLOR_CATEGORIES)
