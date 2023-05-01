# Create database for REST service

Several scripts to process Excel files into a SQLite database for the REST service

* **validateData.py** : validate Excel files for *pedigree* and *resources*
* **constructDatabase.py** : construct a SQLite database from the validated Excel files
* **checkDatabase.py** : check existance of locations and files referred to in the SQLite database

Before running these script, create a file `config.ini` defining the data location for the Excel files and the location for the database and other service data.
```
[PATHS]
data: demo_data
service: demo_service
```

## Excel files

The database is constructed from Excel files:

* File `pedigree.xlsx` describing all varieties
* One or multiple Excel files `*.xlsx` resources linking k-mer databases or marker data to varieties
