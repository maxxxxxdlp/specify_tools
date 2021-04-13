from common import *
import sys

if len(sys.argv) < 2:
    raise Exception("Required argument <in_file_name> is missing")

if len(sys.argv) < 3:
    raise Exception("Required argument <first_column_index> is missing")

if len(sys.argv) < 4:
    raise Exception(
        "Required argument <second_column_index> is missing"
    )

if len(sys.argv) < 4:
    raise Exception("Required argument <out_file_name> is missing")

in_file_name = os.path.join(global_base_dir, sys.argv[1])
first_column_index = int(sys.argv[2])
second_column_index = int(sys.argv[3])
max_column_index = max(first_column_index, second_column_index)
out_file_name = os.path.join(global_base_dir, sys.argv[4])

with open(in_file_name) as file:
    lines = file.read().split("\n")

out_lines = []
for line in lines:

    line_parts = line.split(column_separator)

    if len(line_parts) >= max_column_index:
        (
            line_parts[first_column_index],
            line_parts[second_column_index],
        ) = (
            line_parts[second_column_index],
            line_parts[first_column_index],
        )
        line = column_separator.join(line_parts)

    out_lines.append(line)

with open(out_file_name, "w") as file:
    file.write("\n".join(out_lines))
