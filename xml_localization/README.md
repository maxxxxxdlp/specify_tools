# xml_localization

The scripts in this folder were used during the second phase of localizing
`schema_localization.xml` files.

This README describes various scripts in order they would be used during
a normal workflow

## `config.py`

Configuration options are described in `config.py`.

None of the script

## `populate_workdir.py`

Get all `schema_localization.xml` files from `specify6_location` and move
them into `working_directory`

## `deconstruct.py`

Parses the source files, separates languages into files and removes
redundant strings for easier localization.

This will also validate the source file and show warnings on errors.

On success, several files would be generated in each subdirectory of the
working directory.

The following files should not be edited as they would be used during the
reconstruction process:

- `_original.json` - file containing all English strings as extracted
- `_striped.json` - like `_original.json` but strips whitespace, digits
  and special symbols from the beginning and the end of each string
- `_distinct.json` - like `_striped.json` but all strings are made
  distinct

Besides, there would be an `editable.tsv` file created with strings for
each language that was specified in `config.py`.

The values in all the columns of this file can be edited, but
make sure not to add/remove/swap any lines. Also, make sure not to edit
the first row

## (Optional) `glue_editable_files.py`

Combine all `editable.tsv` into a single `schema_editable.tsv` file
located in the workdir.

The values in all the columns of this file can be edited, but
make sure not to add/remove/swap any lines. Also, make sure not to edit
the first row or the lines that specify the name of each
`editable.tsv` file

## Translate files

Use any external editor to modify all `editable.tsv` files or
main `schema_editable.tsv` file.

## (Optional) `unglue_editable_files.py`

Opposite of `glue_editable_files.py`
Separate `schema_editable.tsv` into `editable.tsv` files that would be
put into their respective subdirectories of the working directory

## `reconstruct.py`

After `editable.tsv` was modified, it's time to validate it and
reconstruct it all back into a single schema xml file.

Before running the script, make sure that `schema_localization.xml`,
`_original.json`, `_striped.json` and `_distinct.json` were not modified
accidentally.

The reconstructed file would be called `schema_localization_edited.xml`.

## `push_changes.py`

Move all `schema_localization_edited.xml` files back into the Specify
directory.

## `show_localization_errors.py`

This script would be able to show common localization errors and propose
to fix them automatically
