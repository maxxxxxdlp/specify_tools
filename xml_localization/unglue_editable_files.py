import os

from termcolor import colored

from xml_localization.relocalization import config

with open(
    os.path.join(
        os.getcwd(),
        config.working_directory,
        config.schema_editable_file_name,
    )
) as file:
    content = file.read()

split_content = content.split(config.schema_edited_file_separator)
parsed_strings = [
    string.split(config.line_separator, 1) for string in split_content
]

for directory_name, file_content in parsed_strings:
    target_file_location = os.path.join(
        os.getcwd(),
        config.working_directory,
        directory_name.strip(),
        config.editable_file_name,
    )
    with open(target_file_location, "w") as file:
        print(
            "%s (%d lines)"
            % (
                colored(target_file_location, "green"),
                len(file_content.split(config.line_separator)),
            )
        )
        file.write(file_content)
