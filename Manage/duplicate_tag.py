import os
import sys

def remove_specific_duplicate_tags(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")  # Debug print

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Find the second '---' marker
                try:
                    second_dash_index = lines.index("---\n", lines.index("---\n") + 1)
                except ValueError:
                    print(f"No second '---' found in {file_path}")  # Debug print
                    continue

                # Find the first tag after the second '---'
                first_tag = None
                for i in range(second_dash_index + 1, len(lines)):
                    if lines[i].startswith("#[["):
                        first_tag = lines[i]
                        print(
                            f"First tag found: {first_tag.strip()} in {file_path}"
                        )  # Debug print
                        break

                # Eliminate subsequent duplicates of the first tag
                if first_tag:
                    lines = (
                        lines[: second_dash_index + 1]
                        + [first_tag]
                        + [
                            line
                            for line in lines[second_dash_index + 1 :]
                            if line != first_tag
                        ]
                    )
                    print(f"Duplicate tags removed in {file_path}")  # Debug print
                else:
                    print(
                        f"No tag found after second '---' in {file_path}"
                    )  # Debug print

                # Write the cleaned content back to the file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)


def update_content_and_position(base_path):
    # Resolve the base_path to an absolute path
    abs_path = os.path.abspath(base_path)
    
    # Check if the resolved absolute path includes 'Library'
    if "Library" not in abs_path:
        print("Error: The path does not include 'Library'. Exiting...")
        sys.exit(1)  # Exit the program with an error code

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")  # Debug print

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                try:
                    first_dash_index = lines.index("---\n")
                    second_dash_index = lines.index("---\n", first_dash_index + 1)
                except ValueError:
                    print(f"Required '---' markers not found in {file_path}")  # Debug print
                    continue

                # Move 'dg-publish: true' if present
                dg_publish_index = None
                for i, line in enumerate(lines[first_dash_index + 1:second_dash_index], start=first_dash_index + 1):
                    if line.strip() == "dg-publish: true":
                        dg_publish_index = i
                        break

                if dg_publish_index is not None:
                    # Remove 'dg-publish: true' and place it right after the first '---'
                    lines.pop(dg_publish_index)
                    lines.insert(first_dash_index + 1, "dg-publish: true\n")

                # Update 'second_dash_index' after potential modification
                second_dash_index = lines.index("---\n", first_dash_index + 1)

                # Remove specific duplicate tags
                first_tag = None
                for i in range(second_dash_index + 1, len(lines)):
                    if lines[i].startswith("#[["):
                        first_tag = lines[i]
                        break

                if first_tag:
                    lines = (
                        lines[:second_dash_index + 1]
                        + [first_tag]
                        + [
                            line for line in lines[second_dash_index + 1:]
                            if line != first_tag
                        ]
                    )

                # Write the cleaned content back to the file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)

# Assuming the script is executed from 'some_path/Library/Manage/pythonfile'
update_content_and_position("..")

# Usage
remove_specific_duplicate_tags("..")
