from common import *
import sys

if len(sys.argv) < 2:
    raise Exception("Required argument <file_name> is missing")

if len(sys.argv) < 3:
    raise Exception("Required argument <column_index> is missing")

file_name = os.path.join(global_base_dir, sys.argv[1])
column_index = int(sys.argv[2])

with open(file_name) as file:
    lines = file.read().split("\n")[1:]

print(
    "\n".join(
        [
            line.split(column_separator)[column_index]
            for line in lines
            if len(line.split(column_separator)) >= column_index
            and line.split(column_separator)[column_index] != ""
        ]
    )
)
