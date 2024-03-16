import re
import yaml
from pathlib import Path


def extract_description_from_md(file_path):
    """Extract description field from markdown file"""
    with file_path.open('r', encoding='utf-8') as md_file:
        content = md_file.read()
        metadata = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        
        
        if metadata:
            extracted_metadata = metadata.group(1)
            # print(f"Extracted YAML:\n {md_file} {extracted_metadata}")  # Diagnostic print
            try:
                data = yaml.safe_load(extracted_metadata)
                description = data.get('description', 'No description provided')
                # print(f"dscription: {description}")  # Diagnostic print
                
                return description
            except yaml.YAMLError as e:
                print(f"YAML Error: {e}")
                return 'None'
        return 'None'

def create_base_template(library_path, output_file,template_file_name='base_template.md'):
    """Navigate the directory structure to extract the description and create base_template.md"""
    
    print(f'***************Start Create base template*************** \nlibrary_path = {library_path} \noutput_file = {output_file} \nTEMPLATE_FILE_NAME = {template_file_name}')

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
    
    print(f'***************Finished!! Create base template *************** \nbase template : library_path = {library_path} \noutput_file = {output_file} \nTEMPLATE_FILE_NAME = {template_file_name}')



