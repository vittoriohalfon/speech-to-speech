import os
import json

# Function to convert text to JSON
def text_to_json(text):
    lines = text.split('\n')
    pair_line = lines.pop(0)  # 'pair' is always the first line
    prompt_line = lines.pop(0)  # 'Prompt:' starts the second line
    # Remove the colon and whitespace from the start of the prompt
    prompt = prompt_line[len('Prompt: '):]
    # The rest of the lines comprise the response. Join them back together.
    response = '\n'.join(lines).strip()
    # Return the data as a JSON-compatible dictionary
    return {"pair": {"Prompt": prompt, "Response": response}}

# Function to remove empty lines
def remove_empty_lines(data):
    for key, value in data.items():
        if isinstance(value, str):
            # Split the string into lines, remove empty lines, then join it back into a string
            lines = value.split('\n')
            non_empty_lines = [line for line in lines if line.strip() != '']
            data[key] = '\n'.join(non_empty_lines)
        elif isinstance(value, dict):
            # Recursively remove empty lines from dictionaries
            remove_empty_lines(value)
        elif isinstance(value, list):
            # Recursively remove empty lines from lists
            for item in value:
                if isinstance(item, dict):
                    remove_empty_lines(item)
    return data

# Function to read and reformat the data
def read_and_reformat(data):
    # Extract the data under the 'pair' key
    pair_data = data["pair"]
    # Reformat the data
    reformatted_data = {"prompt": pair_data["Prompt"], "completion": pair_data["Response"]}
    return reformatted_data

# Directory containing the .json files
directory = "kg_json"

# List to store all the reformatted data
all_data = []

# Iterate over the .json files in the directory
for file in os.listdir(directory):
    if file.endswith(".json"):
        # Load the text data
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Convert the text to JSON
        data = text_to_json(text)

        # Remove empty lines
        data = remove_empty_lines(data)

        # Reformat the data
        reformatted_data = read_and_reformat(data)

        # Add reformatted data to the list
        all_data.append(reformatted_data)
        
        # Save the cleaned JSON data back to the file
        with open(os.path.join(directory, file), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# Save all the reformatted data to a single .json file
with open(os.path.join(directory, "merged_data.json"), "w", encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)
