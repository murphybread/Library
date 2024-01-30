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
def add_tags_to_md_files(base_path, structure):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.readlines()

                    new_tag = construct_tag(file, structure)
                    print(f"Checking tags in {file}")

                    # Split the file into header and body
                    if "---" in content:
                        split_index = content.index(
                            "---\n", 1
                        )  # Find the second occurrence of '---'
                        header = content[: split_index + 1]
                        body = content[split_index + 1 :]

                        # Check if new tag already exists in header
                        if new_tag + "\n" not in header:
                            header.insert(
                                -1, new_tag + "\n"
                            )  # Insert tag at the end of header
                            print(f"Added tag to {file}")

                        # Reassemble the file
                        content = header + body
                    else:
                        print(f"No header in {file}, skipping tag addition")

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(content)

                except UnicodeDecodeError as e:
                    print(f"Error reading {file_path}: {e}")


# Function to construct the appropriate tag for a file
def construct_tag(file_name, structure):
    major_match = re.match(r"(\d0\d).md", file_name)
    minor_match = re.match(r"(\d[1-9]\d)\.md", file_name)
    sub_match = re.match(r"(\d{3}\.\d{2}).md", file_name)
    book_match = re.match(r"(\d{3}\.\d{2}) [a-zA-Z].md", file_name)

    tag = ""
    if major_match:
        major_code = major_match.group(1)
        print(f"Major Category Match: {major_code}")
        tag = construct_major_tag(major_code, structure)

    elif minor_match:
        minor_code = minor_match.group(1)
        print(f"Minor Category Match: {minor_code}")
        tag = construct_minor_tag(minor_code, structure)

    elif sub_match:
        sub_code = sub_match.group(1)
        print(f"Subcategory Match: {sub_code}")
        tag = construct_subcategory_tag(sub_code, structure)

    elif book_match:
        book_code = book_match.group(1)
        print(f"Book Match: {book_code}")
        tag = construct_book_tag(book_code, structure)

    else:
        print(f"No match for file: {file_name}")

    return tag


# Helper functions to construct tags for each file type
def construct_major_tag(major_code, structure):
    tag = f"#[[{major_code}]]"
    minor_categories = structure["MajorCategories"][major_code].get(
        "MinorCategories", {}
    )
    for minor_key in minor_categories.keys():
        tag += f"#[[{minor_key}]]"
    return tag


def construct_minor_tag(minor_code, structure):
    for major_key, major_val in structure["MajorCategories"].items():
        if minor_code in major_val["MinorCategories"]:
            major_value = major_val["value"]
            tag = f"#[[{major_value}]]#[[{minor_code}]]"
            subcategories = major_val["MinorCategories"][minor_code].get(
                "Subcategories", {}
            )
            for sub_key in subcategories.keys():
                tag += f"#[[{sub_key}]]"
            return tag
    return ""


def construct_subcategory_tag(sub_code, structure):
    for major_key, major_val in structure["MajorCategories"].items():
        for minor_key, minor_val in major_val.get("MinorCategories", {}).items():
            if sub_code in minor_val["Subcategories"]:
                tag = f"#[[{sub_code}]]"
                return tag
    return ""


def construct_book_tag(book_code, structure):
    for major_key, major_val in structure["MajorCategories"].items():
        for minor_key, minor_val in major_val.get("MinorCategories", {}).items():
            for sub_key, sub_val in minor_val.get("Subcategories", {}).items():
                if book_code.startswith(sub_key):
                    tag = f"#[[{sub_key}]]#[[{book_code}]]"
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
move_files_from_Entrance(
    Entrance_directory, base_directory, json_structure
)  # Added this line
add_tags_to_md_files(base_directory, json_structure)
