Files in sql directory:

create_tables.sql - Initializes and creates LOST database, tables in sql.

gen_insert.py - Python script to move legacy data into LOST database.

import_data.sh - Executable to curl legacy data, run create_tables.sql, then gen_insert.py



