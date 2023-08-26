# WPMIGRATOR
Tool designed to migrate data between WordPress sites.

# How to use
Install the project dependencies.
```shell
pip install -r requirements.txt
```
Rename the file `database/environment example.py` to `database/environment.py`, inform the data of the origin and destiny databases, and the prefixes of the origin and destiny databases.
```python
ORIGIN_DB = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'toor',
    'database':'site1_db',
    'raise_on_warnings': True
}

DESTINY_DB = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'toor',
    'database':'site2_db',
    'raise_on_warnings': True
}

PREFIXES = {
    'origin': 'wp_',
    'destiny': 'wp_'
}
```

Run the migration tool
```shell
python wpmigrator.py
```