from common import *
from termcolor import colored


def run(dry_run=False):
    files = glob.glob(
        os.path.join(specify6_src_dir_location, "*.properties")
    )
    basenames = [
        os.path.splitext(os.path.basename(file))[0] for file in files
    ]
    target_files = [
        file_name for file_name in basenames if "_" in file_name
    ]

    language_files = []
    for file_name in target_files:
        base_name, language, = (
            file_name[0 : file_name.rfind("_")],
            file_name[file_name.rfind("_") + 1 :],
        )

        if language not in languages:
            continue

        language_files.append(base_name)

    for base_name in language_files:

        file_data = None
        print(colored(base_name, "yellow"))

        for language in languages:
            with open(
                "%s/%s_%s.properties"
                % (specify6_src_dir_location, base_name, language)
            ) as file:
                lines = file.read().split("\n")

                if file_data is None:
                    file_data = []
                    for i in range(0, len(lines)):
                        file_data.append(
                            dict.fromkeys(languages, False)
                        )

                if len(lines) != len(file_data):
                    raise Exception(
                        'Number of lines is not the same between "%s" (%d) and "%s" (%d)'
                        % (
                            languages[0],
                            len(file_data),
                            language,
                            len(lines),
                        )
                    )

                for i, line in enumerate(lines):
                    file_data[i][language] = line

        columns = [["Field Name"] + languages]

        for i, line_data in enumerate(file_data, 1):

            for language in languages:
                if line_data[language] is False:
                    raise Exception(
                        "{} is not defined at {}".format(language, i)
                    )

            if line_data[languages[0]] == "":
                for language in languages:
                    if line_data[language] != "":
                        raise Exception(
                            '%s is "" at %d, but %s has value "%s"'
                            % (
                                languages[0],
                                i,
                                language,
                                line_data[language],
                            )
                        )
                columns.append([])
            elif line_data[languages[0]][0] == "#":
                for language in languages:
                    if (
                        line_data[language] == ""
                        or line_data[language][0] != "#"
                    ):
                        raise Exception(
                            '%s begins with "#" at line %d, but %s has value'
                            % (languages[0], i, language)
                        )
                columns.append([line_data[languages[0]]])
            else:
                key = line_data[languages[0]].split("=")[0]
                columns.append(
                    [key]
                    + list(
                        map(
                            lambda language: strip_key(
                                line_data, key, i, language, languages
                            ),
                            languages,
                        )
                    )
                )

        if not dry_run:
            columns_tsv = "\n".join(
                [column_separator.join(fields) for fields in columns]
            )
            with open(
                os.path.join(
                    global_base_dir,
                    "properties_to_tsv/%s.tsv" % base_name,
                ),
                "w",
            ) as file:
                file.write(columns_tsv)


def process(dry_run=False):
    try:
        run(dry_run)
    except Exception as e:
        print(colored(e, "red"))
        return 1


run(False)
