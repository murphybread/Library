import os
import json
import shutil

def load_json_structure(file_path):
    # Load the JSON file containing the directory structure
    with open(file_path, 'r') as file:
        return json.load(file)
    
    
def create_directories_and_files(base_path, structure):
    for major_key, major_val in structure['MajorCategories'].items():
        major_dir = os.path.join(base_path, major_key)
        os.makedirs(major_dir, exist_ok=True)
        create_md_file(major_dir, major_key)
 
        for minor_key, minor_val in major_val.get('MinorCategories', {}).items():
            minor_dir = os.path.join(major_dir, minor_key)
            os.makedirs(minor_dir, exist_ok=True)
            create_md_file(minor_dir, minor_key)

            for sub_key in minor_val.get('Subcategories', {}):
                sub_dir = os.path.join(minor_dir, sub_key)
                os.makedirs(sub_dir, exist_ok=True)
                create_md_file(sub_dir, sub_key)

def create_md_file(directory, file_name):
    md_file_path = os.path.join(directory, f"{file_name}.md")
    if not os.path.exists(md_file_path):
        with open(md_file_path, 'w') as md_file:
            md_file.write(f"# {file_name}\n\n")  # Example content, can be customized

# Rest of the script remains the same...


def move_files_from_Entrance(Entrance_path, base_path, structure):
    # Check if Entrance directory has any markdown files
    md_files = [f for f in os.listdir(Entrance_path) if f.endswith('.md')]
    if not md_files:
        print("No books to work on.")
        return

    files_moved = 0  # Counter for the number of files moved

   # Move each markdown file to its new location
    for file in md_files:
        if file == "Call Number Index.md":  # Skip the specific file
            continue
        new_path = determine_new_path(file, structure, base_path)
        source_path = os.path.join(Entrance_path, file)

        print(f'Trying to move: {source_path} to {new_path}')

        if new_path:
            print(f'Trying to move: {source_path} to {new_path}')
            shutil.move(source_path, new_path)
            print(f'Moved {file} to {new_path}')
            files_moved += 1

    if files_moved == 0:
        print("No books moved.")

def determine_new_path(file_name, structure, base_path):
    parts = file_name.split(' ')
    subcategory_parts = parts[0].split('.')

    print(f'File name parts: {parts}')
    print(f'Subcategory parts: {subcategory_parts}')

    subcategory_code = parts[0]
    book_suffix = parts[1].replace('.md', '') if len(parts) > 1 else ''

    print(f'Subcategory code: {subcategory_code}')
    print(f'Book suffix: {book_suffix}')

    # Iterate through the JSON structure to find the matching path
    for major_key, major_val in structure['MajorCategories'].items():
        for minor_key, minor_val in major_val.get('MinorCategories', {}).items():
            for sub_key in minor_val.get('Subcategories', {}):
                if sub_key == subcategory_code:
                    major_dir = os.path.join(base_path, major_key)
                    minor_dir = os.path.join(major_dir, minor_key)
                    sub_dir = os.path.join(minor_dir, sub_key)

                    book_key = f'{subcategory_code} {book_suffix}' if book_suffix else subcategory_code
                    print(f'Constructed book key: {book_key}')
                    books = minor_val['Subcategories'][sub_key].get("Books", {})
                    
                    if book_key in books:
                        target_path = os.path.join(sub_dir, file_name)
                        print(f'Matching path found: {target_path}')
                        return target_path

    print("No matching path found")
    return None  # No matching path found







json_file_name = 'structure.json'
json_structure = load_json_structure(json_file_name)
base_directory = os.getcwd()
Entrance_directory = os.path.join(base_directory, 'Entrance')

print(f'json_file_name: {json_file_name}')
print(f'base_directory: {base_directory}')
print(f'Entrance_directory: {Entrance_directory}')
print("*--------------------*")


create_directories_and_files(base_directory, json_structure)
move_files_from_Entrance(Entrance_directory, base_directory, json_structure)
