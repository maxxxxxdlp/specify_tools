import os
from shutil import copyfile
from termcolor import colored
from xml_localization.relocalization import config


for directory in [
    f.path
    for f in os.scandir(
        os.path.join(
            os.getcwd(),
            config.working_directory,
        )
    )
    if f.is_dir()
]:

    base_name = os.path.basename(directory)
    schema_file_path = os.path.join(
        directory, config.updated_source_file_name
    )

    if base_name == "main":
        specify_path = os.path.join(
            config.specify6_location, "config", config.source_file_name
        )
    elif base_name == "workbench":
        specify_path = os.path.join(
            config.specify6_location,
            "config",
            config.wb_source_file_name,
        )
    else:
        specify_path = os.path.join(
            config.specify6_location,
            "config",
            directory,
            config.wb_source_file_name,
        )

    print(
        "%s %s %s"
        % (schema_file_path, colored(" >> ", "green"), specify_path)
    )

    copyfile(schema_file_path, specify_path)
