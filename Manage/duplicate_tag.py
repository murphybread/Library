import os


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


# Usage
remove_specific_duplicate_tags("..")
