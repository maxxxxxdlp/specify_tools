from xml_localization.relocalization import config, utils
from xml_localization.relocalization.error_fixers import pre_reconstruct
import json


def reconstruct(working_dir):

    # read original strings
    original_strings = json.loads(
        utils.read_from_file(working_dir, config.original_file_name)
    )

    # read stripped strings
    stripped_strings = json.loads(
        utils.read_from_file(working_dir, config.striped_file_name)
    )

    # read distinct strings
    distinct_strings = json.loads(
        utils.read_from_file(working_dir, config.distinct_file_name)
    )

    # read translated strings
    editable_strings = utils.spreadsheet_to_dict(
        utils.read_from_file(
            working_dir, config.editable_file_name
        ).strip()
    )

    # reconstruct strings and show validation errors
    updated_distinct_strings = [
        {**distinct_strings_line, **edited_strings_line}
        for distinct_strings_line, edited_strings_line in zip(
            distinct_strings, editable_strings
        )
    ]

    indexed_updated_distinct_strings = utils.index_list_of_dict(
        updated_distinct_strings, "en"
    )

    updated_stripped_strings = [
        {
            **line,
            **utils.exclude_unused_languages(
                indexed_updated_distinct_strings[line["en"]]
            ),
        }
        for line in stripped_strings
    ]

    updated_strings = utils.un_strip_strings(
        original_strings,
        stripped_strings,
        updated_stripped_strings,
        pre_reconstruct.error_callback,
    )

    # updated structure
    updated_structure = utils.update_structure(
        utils.parse_xml(working_dir), updated_strings
    )

    # save xml
    utils.dump_to_file(
        working_dir,
        utils.dict_to_xml(updated_structure),
        config.updated_source_file_name,
    )


utils.loop(reconstruct)
