import re
import yaml
from pathlib import Path

TEMPLATE_FILE_NAME = 'base_template.md'

def extract_description_from_md(file_path):
    """Extract description field from markdown file"""
    with file_path.open('r', encoding='utf-8') as md_file:
        content = md_file.read()
        metadata = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        
        
        if metadata:
            try:
                data = yaml.safe_load(metadata.group(1))
                return data.get('description', 'No description provided')
            except yaml.YAMLError:
                return 'None'
        return 'None'

def create_base_template(library_path, output_file):
    """Navigate the directory structure to extract the description and create base_template.md"""
    descriptions = {}
    pattern = re.compile(r'^\d{3}.*\.md$')
    
    for path in library_path.rglob('*.md'):
        if pattern.match(path.name):
            
            description = extract_description_from_md(path)
            if description:
                relative_path = path.relative_to(library_path)
                descriptions[str(relative_path)] = description

    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    
    with output_file.open('w', encoding='utf-8') as out_file:
        for path, desc in descriptions.items():
            out_file.write(f'## {path}\n description: {desc}\n\n')


# Set the library_path to the Library directory
library_path = Path(__file__).parent.parent

# Set the output_file path to the Librarian directory
output_file = Path(__file__).parent / 'Librarian' / TEMPLATE_FILE_NAME


print(f'***************Start Create base template*************** \nlibrary_path = {library_path} \noutput_file = {output_file} \nTEMPLATE_FILE_NAME = {TEMPLATE_FILE_NAME}')
# Create base_template.md
create_base_template(library_path, output_file)
print(f'***************Finished!! Create base template *************** \nbase template : library_path = {library_path} \noutput_file = {output_file} \nTEMPLATE_FILE_NAME = {TEMPLATE_FILE_NAME}')