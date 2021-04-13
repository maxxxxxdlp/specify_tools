# relocalization/

Scripts that were used for the second wave of localization for the
`UI` componentes

Workflow:

* Convert existing `.properties` files from the specify's src directory
  to `.tsv` files using `properties_to_tsv.py` (outputs files to
  `properties_to_tsv` directory). This also runs validation on the
  files and exits if an error was found
* Convert `.tsv` files to `.xlsx` using external tools
* Edit `.xlsx` files to fix localization errors
* Convert localized `.xlsx` back to `.tsv` using `xlsx_to_tsv.py`
  (reads files from the `xlsx` directory and puts them into the
  `xlsx_to_tsv` directory
* Convert final `.tsv` files back to `.properties` and put them into
  the specify's src directory by running `reconstruct.py` (reads files
  from the `xlsx_to_tsv` directory)
* Run validation on the resulting `.properties` files to see that there
  aren't any errors by running `validate_files.py`
* Use `git diff` or etc to see the changes to the `.properties` files
  to make sure that everything looks alright

## Configuration options

Configuration options are descibed in `config.py`

## Utility files

### swap_column.py

Swaps two columns in a `.tsv` file.

```bash
python3 swap_column.py <in_file_name> <first_column_index> <second_column_index> <out_file_name>
```

Column indexes begin with 0, just because!

### inspect_column.py

Shows non empty values for a column in a `.tsv` file

```bash
python3 inspect_column.py <file_name> <column_index>
```

Column indexes begin with 0
