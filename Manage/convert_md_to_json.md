```run-python
import re
import json
import shutil
import os

def md_to_json(md_file, json_file):
    with open(md_file, 'r') as file:
        lines = file.readlines()

    json_structure = {"MajorCategories": {}}
    current_major = current_minor = current_sub = None

    for i, line in enumerate(lines):
        line = line.strip()  # Remove leading and trailing whitespaces
        if not line or line.startswith("---"):
            continue  # Skip empty lines and metadata lines

        print(f"Processing line {i}: {line}")  # Debug print

        try:
            # Match major, minor, subcategories, and book entries
            major_match = re.match(r'\[\[(\d{3})\]\]\s*(.*)', line)
            minor_match = re.match(r'- \[\[(\d{3})\]\]\s*(.*)', line)
            sub_match = re.match(r'- \[\[(\d{3}\.\d{2})\]\]\s*(.*)', line)
            book_match = re.match(r'- \[\[(\d{3}\.\d{2} [a-zA-Z])\]\]\s*(.*)', line)

            if major_match:
                current_major, title = major_match.groups()
                json_structure["MajorCategories"][current_major] = {"value": current_major, "title": title, "MinorCategories": {}}
                print(f"Major Category: {current_major}, Title: {title}")  # Debug print

            elif minor_match:
                current_minor, title = minor_match.groups()
                json_structure["MajorCategories"][current_major]["MinorCategories"][current_minor] = {"title": title, "Subcategories": {}}
                print(f"Minor Category: {current_minor}, Title: {title}")  # Debug print

            elif sub_match:
                current_sub, title = sub_match.groups()
                json_structure["MajorCategories"][current_major]["MinorCategories"][current_minor]["Subcategories"][current_sub] = {"title": title, "Books": {}}
                print(f"Subcategory: {current_sub}, Title: {title}")  # Debug print

            elif book_match:
                book_code, book_title = book_match.groups()
                json_structure["MajorCategories"][current_major]["MinorCategories"][current_minor]["Subcategories"][current_sub]["Books"][book_code] = book_title
                print(f"Book: {book_code}, Title: {book_title}")  # Debug print

        except Exception as e:
            print(f"Error processing line {i}: '{line}'")
            print(str(e))

    # Save JSON structure to file
    temp_json_path = os.path.join(os.getcwd(), json_file)
    with open(temp_json_path, 'w') as outfile:
        json.dump(json_structure, outfile, indent=4)

    # Move the JSON file to the parent directory
    parent_dir_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    destination_path = os.path.join(parent_dir_path, json_file)
    shutil.move(temp_json_path, destination_path)
    print(f"Moved {json_file} to {destination_path}")

# Usage example
md_file = 'Call Number Index.md'
json_file = 'structure.json'

print(f'Read from {md_file}')
md_to_json(md_file, json_file)
print(f'Output json file is {json_file}')

```