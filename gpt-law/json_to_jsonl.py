import json

# Open the JSON file and load the data
with open('merged_data.json', 'r') as json_file:
    data = json.load(json_file)

# Open the JSONL file (or create it if it doesn't exist)
with open('data.jsonl', 'w') as jsonl_file:
    for record in data:
        # Write each record as a separate line in the JSONL file
        jsonl_file.write(json.dumps(record) + '\n')
