import glob
import os
from config import *

global_base_dir = os.getcwd()


def strip_key(line_data, key, i, language, languages):
    local_key = line_data[language].split("=")[0]
    if key != local_key:
        raise Exception(
            "%s key (%s) is not the same as %s key (%s) at line %d"
            % (language, local_key, languages[0], key, i)
        )
    return line_data[language][line_data[language].find("=") + 1 :]
