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
    # Remove CSS styles and unnecessary content using regex patterns
    for pattern in CSS_PATTERNS:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    # Remove all other HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    # Remove extra whitespace
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

# Save the cleaned and segmented content to a single JSON file
def save_cleaned_content(cleaned_data, output_filepath):
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

# Main function to process the JSON file
def process_json_file(filepath, output_filepath):
    data = load_json(filepath)
    cleaned_data = []

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

    # Save the cleaned and segmented content
    save_cleaned_content(cleaned_data, output_filepath)

# Example usage
input_file = 'crawled/category_ukraine_immigration-ukraine_studying-in-ukraine.json'
output_file = 'cleaned/cleaned_ukraine_studying-in-ukraine.json'

# Ensure the directory for the output file exists
output_directory = os.path.dirname(output_file)
if not os.path.exists(output_directory) and output_directory != '':
    os.makedirs(output_directory)

# Process the input file and save the cleaned and segmented content to the output file
process_json_file(input_file, output_file)

print(f"Cleaned and segmented JSON file is saved at {output_file}")
