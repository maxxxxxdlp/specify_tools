import os

from termcolor import colored

from xml_localization.relocalization import config

content = []

for dir_path, _, filenames in os.walk(
    os.path.join(os.getcwd(), config.working_directory)
):

    for filename in [
        f for f in filenames if f == config.editable_file_name
    ]:

        editable_file = os.path.join(
            dir_path, config.editable_file_name
        )

        print(colored(editable_file, "blue"))

        with open(editable_file) as file:

            content.append(
                "%s%s%s"
                % (
                    dir_path.split("/")[-1],
                    config.line_separator,
                    file.read(),
                )
            )

with open(
    os.path.join(
        os.getcwd(),
        config.working_directory,
        config.schema_editable_file_name,
    ),
    "w",
) as file:
    content.sort()
    file.write(config.schema_editable_file_separator.join(content))
