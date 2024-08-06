import json
import re
from collections import defaultdict

# Load the JSON data from the file
input_file = 'crawled/category_canada_immigration-to-canada_studying-in-canada_medical-dental-canada.json'
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize a dictionary to hold segmented data
segmented_data = defaultdict(list)

# Define regular expressions for different categories
categories = {
    'immigration': re.compile(r'\bمهاجرت\b|\bمهاجرت و اقامت\b'),
    'study': re.compile(r'\bتحصیل\b|\bدانشگاه\b'),
    'work': re.compile(r'\bمهاجرت کاری\b'),
    'investment': re.compile(r'\bسرمایه گذاری\b'),
}

# Function to segment content
def segment_content(content):
    for category, regex in categories.items():
        if regex.search(content):
            return category
    return 'other'

# Process the data and segment content
for entry in data:
    url = entry.get('url')
    title = entry.get('title')
    content = entry.get('content')
    
    category = segment_content(content)
    segmented_data[category].append({
        'url': url,
        'title': title,
        'content': content
    })

# Save segmented data into different JSON files
for category, entries in segmented_data.items():
    output_file = f'{category}.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)

print("Content segmented and exported successfully.")
