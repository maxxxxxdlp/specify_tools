from xml_localization.relocalization import config
from xml_localization.relocalization.error_fixers import missing_en_key


def error_callback(error_type, error_message):
    if error_type == "missing_en_key":
        return missing_en_key.error_callback()
    raise Exception(error_message)


def fix(extracted_strings):
    if config.error_fixers["missing_en_key"] == "off":
        return extracted_strings
    else:
        return missing_en_key.test(extracted_strings)
