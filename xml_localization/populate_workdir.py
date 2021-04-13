import os
from pathlib import Path
from shutil import copyfile

from termcolor import colored

from xml_localization.relocalization import config

base_path = os.path.join(os.getcwd(), config.specify6_location)

for dir_path, _, filenames in os.walk(base_path):
    for filename in [
        f
        for f in filenames
        if f == config.source_file_name
        or f == config.wb_source_file_name
    ]:
        directory = dir_path.split("/")[-1]

        if directory == "config":
            if filename == config.source_file_name:
                directory = "main"
            if filename == config.wb_source_file_name:
                directory = "workbench"

        source = os.path.join(dir_path, filename)
        destination = os.path.join(
            os.getcwd(),
            config.working_directory,
            directory,
            config.source_file_name,
        )

        print(
            "{} {} {}".format(
                source, colored(" >> ", "green"), destination
            )
        )

        Path(os.path.dirname(destination)).mkdir(
            parents=True, exist_ok=True
        )

        copyfile(source, destination)
