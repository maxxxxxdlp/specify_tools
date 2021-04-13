import glob

final_content = ""

for file_name in glob.glob("./properties_to_tsv/*.tsv"):
    with open(file_name) as file:
        content = file.read()
    final_content += "~~~~~~~\n{}\n{}\n".format(file_name, content)

with open("joined_files.tsv", "w") as file:
    file.write(final_content)
