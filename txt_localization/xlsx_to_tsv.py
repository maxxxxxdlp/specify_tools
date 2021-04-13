from common import *
import pandas as pd


def xlsx_to_tsv(in_file_name, out_file_name):
    data_xls = pd.read_excel(
        in_file_name, engine="openpyxl", dtype=str, index_col=None
    )
    data_xls.to_csv(
        out_file_name,
        encoding="utf-8",
        index=False,
        sep=column_separator,
    )


def inspect_headers(tsv_file_name):
    with open(tsv_file_name) as file:
        first_line = file.read().split("\n")[0]

    print("{}: {}".format(tsv_file_name, first_line))


def format_in_file_name(file_name):
    return os.path.join(global_base_dir, "xlsx/%s.xlsx" % file_name)


def format_out_file_name(file_name):
    return os.path.join(
        global_base_dir, "xlsx_to_tsv/%s.tsv" % file_name
    )


files = glob.glob(os.path.join(global_base_dir, "xlsx/*.xlsx"))
file_names = [os.path.basename(file) for file in files]
file_base_names = [os.path.splitext(file)[0] for file in file_names]

for file in file_base_names:
    in_file_name = format_in_file_name(file)
    out_file_name = format_out_file_name(file)

    xlsx_to_tsv(in_file_name, out_file_name)
    inspect_headers(out_file_name)
