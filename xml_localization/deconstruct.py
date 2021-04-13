from xml_localization.relocalization import config, utils
from xml_localization.relocalization.error_fixers import pre_deconstruct


def deconstruct(working_dir):
    # parse xml
    source = utils.parse_xml(working_dir)

    # extract strings
    extracted_strings = utils.parse_structure(
        source, pre_deconstruct.error_callback
    )

    # validate & fix errors
    fixed_extracted_strings = pre_deconstruct.fix(extracted_strings)

    # save original strings
    utils.dump_to_json(
        working_dir, fixed_extracted_strings, config.original_file_name
    )

    # strip strings
    striped_strings = utils.strip_strings(fixed_extracted_strings)

    # save striped strings
    utils.dump_to_json(
        working_dir, striped_strings, config.striped_file_name
    )

    # make strings distinct
    distinct_strings = utils.unique_strings(striped_strings)

    # save distinct strings
    utils.dump_to_json(
        working_dir, distinct_strings, config.distinct_file_name
    )

    # save editable strings
    utils.dump_to_file(
        working_dir,
        utils.dict_to_spreadsheet(distinct_strings),
        config.editable_file_name,
    )


utils.loop(deconstruct)
