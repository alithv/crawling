import json
import re
import os
from hazm import Normalizer, sent_tokenize

# Regex patterns for cleaning CSS and styles
CSS_PATTERNS = [
    r'\.elementor[^{}]*\{[^}]*\}',
    r'body\.rtl\s*[^{}]*\{[^}]*\}',
    r'\.hm_boxlink\s*[^{}]*\{[^}]*\}',
    r'@media\s*\([^\{\}]*\)\s*\{[^}]*\}',
    r'body\s*:\s*not\s*\(\.rtl\)[^{}]*\{[^}]*\}',
    r'(\.[a-zA-Z0-9_-]+\s*\{[^}]*\}){2,}',
]

# Function to clean up styles and unnecessary tags with regex
def clean_content(content):
    for pattern in CSS_PATTERNS:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'\s+', ' ', content).strip()
    return content

# Function to normalize Persian text
def normalize_text(text):
    normalizer = Normalizer()
    return normalizer.normalize(text)

# Function to filter out non-Persian content
def filter_persian(text):
    return re.sub(r'[^\u0600-\u06FF\s]', '', text)

# Function to segment Persian text
def segment_text(text):
    sentences = sent_tokenize(text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Load the JSON file
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Save the cleaned and segmented content to a JSON file
def save_cleaned_content(cleaned_data, output_filepath):
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

# Process a single JSON file
def process_json_file(filepath, output_directory):
    data = load_json(filepath)
    cleaned_data = []

    # Extract country information from the filename
    filename = os.path.basename(filepath)
    filename_parts = filename.split('_')

    if len(filename_parts) < 2:
        print(f"Filename does not contain expected parts: {filename}")
        return

    country_name = filename_parts[1]  # Adjust based on your file structure

    # Ensure the output directory for this country exists
    country_output_directory = os.path.join(output_directory, country_name)
    if not os.path.exists(country_output_directory):
        os.makedirs(country_output_directory)

    # Iterate through each dictionary in the list
    for entry in data:
        content = clean_content(entry.get('content', ''))
        normalized_content = normalize_text(content)
        filtered_content = filter_persian(normalized_content)
        segmented_content = segment_text(filtered_content)
        cleaned_entry = {
            'url': entry.get('url'),
            'title': entry.get('title'),
            'segments': segmented_content
        }
        cleaned_data.append(cleaned_entry)

    # Save the cleaned and segmented content to a JSON file
    output_filepath = os.path.join(country_output_directory, f'cleaned_{os.path.basename(filepath)}')
    save_cleaned_content(cleaned_data, output_filepath)

# Process all specified JSON files
def process_multiple_json_files(filepaths, output_directory):
    for filepath in filepaths:
        process_json_file(filepath, output_directory)

# Function to find all JSON files in the 'crawled' directory
def find_json_files(directory):
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

# Example usage
crawled_directory = 'crawled'
output_directory = 'cleaned'
input_files = find_json_files(crawled_directory)

# Process all found JSON files
process_multiple_json_files(input_files, output_directory)

print(f"All JSON files in the '{crawled_directory}' directory have been processed and saved in the '{output_directory}' directory.")
