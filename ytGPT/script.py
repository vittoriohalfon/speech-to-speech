import re

def clean_text(file_path, output_path):
    # Regular expression to match timestamps in the format HH:MM:SS.mmm and backslashes at the end of lines
    timestamp_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}'
    backslash_pattern = r'\\$'

    # Read the input file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Remove timestamps, backslashes at the end of lines, and leading spaces from each line
    cleaned_content = [re.sub(timestamp_pattern, '', line) for line in content]
    cleaned_content = [re.sub(backslash_pattern, '', line).lstrip() for line in cleaned_content]

    # Write the cleaned content to a new file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(cleaned_content)

# Define the input and output file paths
input_file_path = './script.txt.rtf'  # Replace with your file path
output_file_path = './cleaned_script.txt'  # Choose where to save the cleaned file

# Clean the text
clean_text(input_file_path, output_file_path)
