from xml_localization.relocalization.error_fixers import (
    unexpected_affix,
)


def error_callback(error_type, error_message, error_payload):
    if error_type == "unexpected_affix":
        return unexpected_affix.error_callback(
            error_message, error_payload
        )
    raise Exception(error_message)
