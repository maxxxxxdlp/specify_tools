import copy
import json
import os
import re
from collections import defaultdict
import xmltodict
from termcolor import colored
import xml.dom.minidom
from xml_localization.relocalization import config

defined_languages = config.languages.keys()


def loop(function):
    base_dir = os.path.join(os.getcwd(), config.working_directory)

    for directory in os.listdir(base_dir):

        full_path = os.path.join(base_dir, directory)

        if not os.path.isdir(full_path):
            continue

        print(colored(full_path.split("/")[-1], "blue"))
        function(full_path)


def parse_xml(working_location):
    with open(
        os.path.join(working_location, config.source_file_name)
    ) as source_file:
        return xmltodict.parse(source_file.read())


def dump_to_json(working_location, source, file_name):
    dump_to_file(
        working_location,
        json.dumps(
            source, indent=4, sort_keys=False, ensure_ascii=False
        ),
        file_name,
    )


def dump_to_file(working_location, source: str, file_name):
    with open(os.path.join(working_location, file_name), "w") as file:
        file.write(source)


def read_from_file(working_location, file_name):
    with open(os.path.join(working_location, file_name)) as file:
        return file.read()


exclude_unused_languages = lambda line: {
    key: value for key, value in line.items() if key in config.languages
}


def traverse_string(list_of_str, callback):
    for string in list_of_str:
        if "text" in string:
            callback(string)


def traverse_strings(structure, path, callback):
    for branch in ["names", "descs"]:
        if branch in structure and structure[branch] is not None:

            if not isinstance(structure[branch]["str"], list):
                structure[branch]["str"] = [structure[branch]["str"]]

            callback(
                structure[branch]["str"], "{} > {}".format(path, branch)
            )


def traverse_structure(structure, callback):
    if not isinstance(structure["vector"]["container"], list):
        structure["vector"]["container"] = [
            structure["vector"]["container"]
        ]

    for container in structure["vector"]["container"]:

        callback(container, container["@name"])

        if "items" not in container or container["items"] is None:
            continue

        if not isinstance(container["items"]["desc"], list):
            container["items"]["desc"] = [container["items"]["desc"]]

        for desc in container["items"]["desc"]:
            callback(
                desc,
                "{} > {}".format(container["@name"], desc["@name"]),
            )


def parse_structure(structure, error_callback):
    extracted_strings = []

    def traverse_structure_callback(container_obj, container_name):
        nonlocal extracted_strings

        extracted_strings = []

        def traverse_strings_callback(structure_obj, path):
            nonlocal extracted_strings

            extracted_line = {}

            def traverse_string_callback(string):
                nonlocal extracted_line

                extracted_line[string["@language"]] = string["text"]

                pass

            extracted_strings += traverse_string(
                structure_obj, traverse_string_callback
            )

            if not len(extracted_line.keys()):
                return []

            if "en" not in extracted_line and error_callback:
                response = error_callback(
                    "missing_en_key",
                    "%s strings for english language are missing %s. location: %s"
                    % (
                        colored("error: ", "red"),
                        json.dumps(
                            extracted_line, indent=4, sort_keys=False
                        ),
                        path,
                    ),
                )

                if isinstance(response, str):
                    extracted_line["en"] = response

            for language in defined_languages:
                if language not in extracted_line:
                    extracted_line[language] = ""

        extracted_strings += traverse_strings(
            container_obj, container_name, traverse_strings_callback
        )

    traverse_structure(structure, traverse_structure_callback)

    return extracted_strings


def update_structure(structure, updated_strings):

    line_index = 0

    def update_structure_callback(container_obj, container_name):
        def update_strings_callback(structure_obj, _):

            nonlocal line_index

            line = updated_strings[line_index].copy()

            def update_string_callback(line_string):

                if line[line_string["@language"]] is None:
                    return

                line_string["text"] = line[line_string["@language"]]
                line[line_string["@language"]] = None

            traverse_string(structure_obj, update_string_callback)

            for language_code, string in line.items():
                if string is None:
                    continue
                structure_obj.append(
                    {
                        **{
                            "@" + key: value
                            for key, value in config.languages[
                                language_code
                            ]["xml_attributes"].items()
                        },
                        "text": string,
                    }
                )

            line_index += 1

        traverse_strings(
            container_obj, container_name, update_strings_callback
        )

    traverse_structure(structure, update_structure_callback)

    return structure


# based on https://gist.github.com/reimund/5435343/#gistcomment-2663720
def dict2xml(d, root_node=None):
    wrap = False if None == root_node or isinstance(d, list) else True
    root = "root" if None == root_node else root_node
    root_singular = (
        root[:-1] if "s" == root[-1] and None == root_node else root
    )
    xml_str = ""
    attr = ""
    children = []

    if isinstance(d, dict):
        for key, value in dict.items(d):
            if isinstance(value, dict):
                children.append(dict2xml(value, key))
            elif isinstance(value, list):
                children.append(dict2xml(value, key))
            elif key[0] == "@":
                attr = attr + " " + key[1::] + '="' + str(value) + '"'
            elif value is None:
                children.append("<" + key + "/>")
            else:
                xml_str = (
                    "<" + key + ">" + str(value) + "</" + key + ">"
                )
                children.append(xml_str)

    else:
        for value in d:
            children.append(dict2xml(value, root_singular))

    end_tag = ">" if 0 < len(children) else "/>"

    if wrap or isinstance(d, dict):
        xml_str = "<" + root + attr + end_tag

    if 0 < len(children):
        for child in children:
            xml_str = xml_str + child

        if wrap or isinstance(d, dict):
            xml_str = xml_str + "</" + root + ">"

    return xml_str


def dict_to_xml(structure):
    return xml.dom.minidom.parseString(
        dict2xml(structure["vector"], root_node="vector"),
    ).toprettyxml(indent="  ")


def dict_to_spreadsheet(structure) -> str:
    languages_to_include = config.languages.keys()
    spreadsheet = [languages_to_include]

    for line in structure:
        spreadsheet_row = []
        for language in languages_to_include:
            spreadsheet_row.append(
                line[language] if language in line else ""
            )
        spreadsheet.append(spreadsheet_row)

    return config.line_separator.join(
        [config.column_separator.join(line) for line in spreadsheet]
    )


def spreadsheet_to_dict(spreadsheet: str):
    languages_to_include = config.languages.keys()
    lines = spreadsheet.split(config.line_separator)[1:]

    return [
        {
            language: cell
            for language, cell in zip(
                languages_to_include,
                line.split(config.column_separator),
            )
        }
        for line in lines
    ]


def prompt(question):
    response = input("%s " % question)
    return response.lower() in ["y", "yes", "true", "t", "1"]


substr = lambda string, position: string[position[0] : position[1]]


def re_search(regex_pattern, string):
    match = re.search(regex_pattern, string, re.IGNORECASE)

    if not match:
        return ""

    else:
        return match.group()


def strip_strings(extracted_strings):
    stripped_strings = copy.deepcopy(extracted_strings)
    regex = r"[^%s]+" % config.full_charset

    for index, line in enumerate(stripped_strings):

        for position in ["start", "end"]:
            regex_pattern = (
                "^%s" if position == "start" else "%s$"
            ) % regex

            for (
                language_code,
                language_config,
            ) in config.languages.items():

                if language_code not in line:
                    continue

                local_match = re_search(
                    regex_pattern, line[language_code]
                )

                if local_match:
                    stripped_strings[index][language_code] = substr(
                        stripped_strings[index][language_code],
                        [len(local_match), None]
                        if position == "start"
                        else [0, -len(local_match)],
                    )

    return stripped_strings


def unique_strings(striped_strings):
    distinct_strings_dict = {}

    for line in striped_strings:
        if line["en"] in distinct_strings_dict:
            continue
        else:
            distinct_strings_dict[line["en"]] = line

    return list(distinct_strings_dict.values())


index_list_of_dict = lambda list_of_dict, index_key: {
    line[index_key]: line for line in list_of_dict
}


def un_strip_strings(
    original_strings,
    stripped_strings,
    updated_stripped_strings,
    error_callback,
):

    updated_strings = []
    regex = r"[^%s]+" % config.full_charset

    for original_line, updated_stripped_line in zip(
        original_strings, updated_stripped_strings
    ):

        updated_line = updated_stripped_line.copy()
        stripped_parts = defaultdict(dict)

        for line_variant_name, line_variant in [
            ["original_line", original_line],
            ["updated_stripped_line", updated_stripped_line],
        ]:
            for position in ["start", "end"]:

                regex_pattern = (
                    "^%s" if position == "start" else "%s$"
                ) % regex

                for language_code in config.languages.keys():

                    if language_code not in line_variant:
                        continue

                    if (
                        line_variant_name == "original_line"
                        and language_code != "en"
                    ):
                        continue

                    match = re_search(
                        regex_pattern, line_variant[language_code]
                    )

                    if (
                        language_code
                        not in stripped_parts[line_variant_name]
                    ):
                        stripped_parts[line_variant_name][
                            language_code
                        ] = defaultdict(dict)

                    stripped_parts[line_variant_name][language_code][
                        position
                    ] = match

        for language_code, stripped_language_parts in stripped_parts[
            "updated_stripped_line"
        ].items():
            for position, match in stripped_language_parts.items():

                response = "original_en"
                if match != "":
                    response = error_callback(
                        "unexpected_affix",
                        (
                            '%s String for %s language (%s) has an affix "%s" at the '
                            + "%s even though it is not supposed to\n"
                            + "Original line: %s\n"
                            + "Updated line: %s\n"
                        )
                        % (
                            colored("ERROR: ", "red"),
                            language_code,
                            updated_stripped_line[language_code],
                            match,
                            position,
                            json.dumps(
                                original_line,
                                indent=4,
                                ensure_ascii=False,
                            ),
                            json.dumps(
                                updated_stripped_line,
                                indent=4,
                                ensure_ascii=False,
                            )
                            # TODO: highlight current record
                            # TODO: don't prompt if match is the same as EN
                        ),
                        [
                            original_line,
                            updated_stripped_line,
                            language_code,
                        ],
                    )

                    if response == "current_language":
                        pass
                    else:
                        if response == "current_en":
                            stripped_parts["original_line"]["en"][
                                position
                            ] = stripped_parts["updated_stripped_line"][
                                "en"
                            ][
                                position
                            ]

                        if position == "start":
                            updated_line[language_code] = updated_line[
                                language_code
                            ][len(match) :]
                        else:
                            updated_line[language_code] = updated_line[
                                language_code
                            ][: -1 * len(match)]

                if response != "current_language":
                    if position == "start":
                        updated_line[language_code] = (
                            stripped_parts["original_line"]["en"][
                                position
                            ]
                            + updated_stripped_line[language_code]
                        )
                    else:
                        updated_line[language_code] = (
                            updated_stripped_line[language_code]
                            + stripped_parts["original_line"]["en"][
                                position
                            ]
                        )

                # TODO: implement other error fixers here

        updated_strings.append(updated_line)

    return updated_strings
