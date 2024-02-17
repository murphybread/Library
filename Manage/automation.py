import os
import json
import shutil
import re

import convert_md_to_json


# Load the JSON file containing the directory structure
def load_json_structure(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


# Create directories based on the JSON structure
def create_directories(base_path, structure):
    for major_key, major_val in structure["MajorCategories"].items():
        major_dir = os.path.join(base_path, major_key)
        os.makedirs(major_dir, exist_ok=True)
        for minor_key in major_val.get("MinorCategories", {}):
            minor_dir = os.path.join(major_dir, minor_key)
            os.makedirs(minor_dir, exist_ok=True)
            subcategories = major_val["MinorCategories"][minor_key].get(
                "Subcategories", {}
            )
            for sub_key in subcategories:
                sub_dir = os.path.join(minor_dir, sub_key)
                os.makedirs(sub_dir, exist_ok=True)


def move_files_from_Entrance(Entrance_path, base_path, structure):
    # Check if Entrance directory has any markdown files
    md_files = [f for f in os.listdir(Entrance_path) if f.endswith(".md")]
    if not md_files:
        print("No books to work on.")
        return

    files_moved = 0  # Counter for the number of files moved

    # Move each markdown file to its new location
    for file in md_files:
        new_path = determine_new_path(file, structure, base_path)
        source_path = os.path.join(Entrance_path, file)

        print(f"Trying to move: {source_path} to {new_path}")

        if new_path:
            print(f"Trying to move: {source_path} to {new_path}")
            shutil.move(source_path, new_path)
            print(f"Moved {file} to {new_path}")
            files_moved += 1

    if files_moved == 0:
        print("No books moved.")


def determine_new_path(file_name, structure, base_path):
    # Remove file extension and split the filename into parts
    parts = file_name.replace(".md", "").split(" ")
    subcategory_code = parts[0]
    book_suffix = parts[1] if len(parts) > 1 else None

    print(f"Processing file: {file_name}")
    print(f"Subcategory code: {subcategory_code}, Book suffix: {book_suffix}")

    # Iterate through the JSON structure to find the matching path
    for major_key, major_val in structure["MajorCategories"].items():
        # Check if file matches a major category
        if subcategory_code == major_key:
            path = os.path.join(base_path, major_key, file_name)
            print(f"Matched major category. Path: {path}")
            return path

        for minor_key, minor_val in major_val.get("MinorCategories", {}).items():
            # Check if file matches a minor category
            if subcategory_code == minor_key:
                path = os.path.join(base_path, major_key, minor_key, file_name)
                print(f"Matched minor category. Path: {path}")
                return path

            for sub_key in minor_val.get("Subcategories", {}):
                # Check if file matches a subcategory or book within a subcategory
                if sub_key == subcategory_code or (
                    book_suffix and f"{sub_key} {book_suffix}" == subcategory_code
                ):
                    sub_dir = os.path.join(base_path, major_key, minor_key, sub_key)
                    path = os.path.join(sub_dir, file_name)
                    print(f"Matched subcategory/book. Path: {path}")
                    return path

    print(f"No matching path found for: {file_name}")
    return None


# Function to add tags to Markdown files
def add_tags_to_md_files(base_path):
    print(f'start add_tags_to_md files')
    for root, dirs, files in os.walk(base_path):
        if "Entrance" not in root:  # Skip processing if not in the Entrance directory
            continue
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r+", encoding="utf-8") as f:
                        content = f.read()
                        f.seek(0)  # Go back to the start of the file
                        
                        new_tag = construct_tag(file)
                        print(f'new_tag: {new_tag}')
                        
                        if "---" in content and new_tag:
                            parts = content.split("---", 2)
                            if len(parts) == 3:
                                header, middle, body = parts
                                modified_middle = f"{middle}---\n{new_tag}\n"
                                new_content = f"{header}---{modified_middle}{body}"
                                f.write(new_content)
                                f.truncate()  # Remove the rest of the old content
                                print(f"Added tag to {file}")
                        else:
                            print(f"No header found in {file}, skipping.")

                except UnicodeDecodeError as e:
                    print(f"Error reading {file}: {e}")

# Tag is Defined by file name
def construct_tag(file_name):
    match = re.match(r"(\d{3})\.(\d{2})\s([a-zA-Z]+)\.md", file_name)
    if match:
        major, minor, subcategory_letter = match.groups()
        
        # Calculate broader category with correction for leading zeroes
        broader_category_num = int(major) - int(major) % 100
        broader_category = f"{broader_category_num:03}"  # Ensure the broader category is zero-padded to 3 digits
        
        major_category = f"{major}"
        subcategory = f"{major}.{minor}"
        book_category = f"{major}.{minor} {subcategory_letter}"
        
        tag = f"#[[{broader_category}]]#[[{major_category}]]#[[{subcategory}]]#[[{book_category}]]"
        return tag
    return ""




# Ensure that we are in the correct directory to prevent affecting other directories
current_dir = os.getcwd()
expected_dir_name = "Library"

if expected_dir_name not in current_dir:
    print(
        f"Error: Current directory {current_dir} is not '{expected_dir_name}'. Exiting script."
    )
    exit()


# Main execution
base_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
json_file_name = "structure.json"


# start convert md
md_file = "../Entrance/Call Number Index.md"
json_file = "structure.json"

print(f"Read from {md_file}")
convert_md_to_json.md_to_json(md_file, json_file)
print(f"Output json file is {json_file}")

# end convert md

json_structure = load_json_structure(json_file_name)
Entrance_directory = os.path.join(base_directory, "Entrance")


print(f"json_file_name: {json_file_name}")
print(f"base_directory: {base_directory}")
print(f"Entrance_directory: {Entrance_directory}")
print("*--------------------*")

create_directories(base_directory, json_structure)
add_tags_to_md_files(Entrance_directory)
move_files_from_Entrance(
    Entrance_directory, base_directory, json_structure
)  # Added this line



