import os

with open("joined_files_edited.tsv") as file:
    final_content = file.read()

split_strings = final_content.split("~~~~~~~\t\t\n./properties_to_tsv/")
parsed_strings = [
    string.split("\t\t\n", 1) for string in split_strings if string
]


for file_name, file_content in parsed_strings:
    print("%s (%d lines)" % (file_name, len(file_content.split("\n"))))
    with open(os.path.join("xlsx_to_tsv/", file_name), "w") as file:
        file.write(file_content)
