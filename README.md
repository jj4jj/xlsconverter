xlsconverter
============

a simple tools convert xls file to protobuffer file  .

#it's gameconfloader new edition (not compatiable)

a converter that convert many xls files to a binary file or text file to supporting program reading .
the xls schema described by protobuf .

##usage
* Environment requiration
 - python 2.6 later need
 - protobuf-python need installed
	- U can get it in github google , then setup.py build/install
 - xlrd python module need installed
* Let your data ready
 - add the table entry description file <demo_desc.py> into 'meta' dir
 - add your excel data files into 'xls' dir
* Orgonize your file with editing the convert talbe description
 - edit conf.py add your convert files description (reffer to demo)
* Convert it !
```sh
$python converter.py
```
##todo list
* Data keywords map a real data
* A friendly GUI


