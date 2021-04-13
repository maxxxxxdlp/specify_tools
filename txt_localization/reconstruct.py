from common import *

files = glob.glob(os.path.join(global_base_dir, "xlsx_to_tsv/*.tsv"))
file_names = [os.path.basename(file) for file in files]
file_base_names = [os.path.splitext(file)[0] for file in file_names]

# If true and forth column is not empty:
#   new strings would be read from the forth column
# else:
# 	reads from the second column
has_forth_column = False


def process_file(in_file_name, out_file_name):

    print("{} >>> {}".format(in_file_name, out_file_name))

    with open(in_file_name) as file:
        lines = file.read().split("\n")

    lines = lines[1:]
    out_lines = []

    for line in lines:

        split_line = line.split(column_separator)

        if split_line[0] == "" or split_line[0][0] == "#":
            out_lines.append(split_line[0])
            continue

        if has_forth_column and split_line[3] and split_line[3] == "":
            split_line[3] = split_line[2]

        key_name, new_localized_variant = (
            split_line[0],
            split_line[2 + int(has_forth_column)],
        )
        out_lines.append(
            "{}={}".format(key_name, new_localized_variant)
        )

    with open(out_file_name, "w") as out_file:
        out_file.write("\n".join(out_lines))


[
    process_file(
        os.path.join(global_base_dir, "xlsx_to_tsv/%s.tsv" % file),
        os.path.join(
            specify6_src_dir_location,
            "{}_{}.properties".format(file, language_prefix),
        ),
    )
    for file in file_base_names
]
