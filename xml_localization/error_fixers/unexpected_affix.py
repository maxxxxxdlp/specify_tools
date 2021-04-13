from xml_localization.relocalization import config


def error_callback(error_message, error_payload):
    original_line, updated_stripped_line, language_code = error_payload

    fixer_mode = config.languages[language_code]["error_fixers"][
        "unexpected_affix"
    ]

    if fixer_mode == "off":
        return "current_language"
    elif fixer_mode == "automatic":
        return "original_en"

    options = [
        "1. Use affix from the original EN string",
        "2. Use affix from the new EN string",
    ]

    if language_code != "en":
        options.append("3. Use affix from the current language")

    result = input(
        (
            "%s\n"
            + "Which affix should be used to fix this error?\n"
            + "%s"
        )
        % (error_message, "\n".join(options))
    )

    if result == "1":
        return "original_en"

    elif result == "2":
        return "new_en"

    else:
        return "current_language"
