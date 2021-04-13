import json
from termcolor import colored
from xml_localization.relocalization import config, utils

# config
number_of_missing_en_strings = 0


def error_callback():
    global number_of_missing_en_strings
    number_of_missing_en_strings += 1
    return False


def test(extracted_strings):
    global number_of_missing_en_strings

    if number_of_missing_en_strings == 0:
        return extracted_strings

    for index, line in enumerate(extracted_strings):
        if "en" not in line or line["en"] == "":
            key = (
                config.stable_key
                if config.stable_key in line
                else list(line.keys())[0]
            )
            print(
                colored(
                    "English string is missing for line %s"
                    % json.dumps(
                        line,
                        indent=4,
                        sort_keys=False,
                        ensure_ascii=False,
                    ),
                    "red",
                )
            )
            for search_line in extracted_strings:
                if key in search_line and search_line[key] == line[key]:

                    accept_fix = config.error_fixers[
                        "missing_en_key"
                    ] == "automatic" or utils.prompt(
                        "Replacement `%s` was found. Accept?"
                        % search_line["en"]
                    )

                    extracted_strings[index]["en"] = (
                        search_line["en"]
                        if accept_fix
                        else input("Type your variant: ")
                    )

                    if accept_fix:
                        print(
                            colored(
                                "FIXED with %s"
                                % extracted_strings[index]["en"],
                                "green",
                            )
                        )

                    break

            if "en" not in extracted_strings[index]:
                extracted_strings[index]["en"] = input(
                    "Type your variant: "
                )

    return extracted_strings
