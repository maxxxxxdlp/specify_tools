# file_gen.php

This script generates `.csv` files full of data according to different parameters

The script accepts the following GET parameters:

- count //how many lines to generate (excluding the header)
- to_file - // if set to 1, the script will prompt the browser to download the resulting file. if set to 0, the result will be shown as plain text

Also, there are following options inside the file:

```php
$FILE_NAME = $count.'_localities.csv'; //file naming format. default will look like 7000_localities.csv, if the $count is 7000
$cols = 5; //how many columns there are
$array = []; //predefined rules go here (see below)
$all_rows_same = !true; //will make each line consist of the $default_value. Otherwise will line number and predefined rules
$default_value = 1;
```

There also is a support for predefined rules:

```php
//[func_name,[param1,param2,...] // you can create and call your own functions
//'static_val' // static value for all cells of that column
//'' - use def if defined. else use $i

//example usage
$array[1] = ['custom_rand', [-90000, 90000, 1000]]; // this will make each cell in 2nd column call the custom_rand(-90000, 90000, 1000) function
$array[2] = 'Point';
$array[3] = '';
```

Currently, there is no support for specifying column headings, but they can be edited easily in a resulting file
