# The SQLite Program

Two modes to the sqlite software:

- Shell Mode:
  Type `sqlite3` in command prompt to create an in memory db.  
  `sqlite3 db.sqlite` saves the db to file.

  Exit the shell with `.exit` or `.e`.

- Command-line Mode:
  Ideal for shell scripts for automated database administration.
  `sqlite3 -help`  
  `sqlite3 [OPTIONS] FILENAME [SQL]`

  A list of options; a db filename; SQL command.

## Database Administration

### Create a database

`sqlite3 test.db` -> doesn't actually create database until you put something in it.

### Create tables

`sqlite> create table test (id integer primary key, value text);`

Creates two columns:

- primary key column 'id' -> increases automatically
- text field called 'value'

### Insert Data

`sqlite> insert into test (id, value) values (1, 'eenie');`  
`sqlite> insert into test (id, value) values (2, 'meenie');`  
`sqlite> insert into test (value) values ('minie');`  
`sqlite> insert into test (value) values ('mo');`

> The `integer primary key` combination allows for auto incrementing of the primary key.
>
> Can use `select last_insert_rowid();` to get the last id added.

`sqlite> .mode column`  
`sqlite> .headers on`

### Getting Data

`sqlite> select * from test;`

### Getting Schema

- `.tables`
- `.indices test`
- `.schema test`
- `.schema`

You can get more info from the `sqlite_master`.

`select type, name, table_name, sql from sqlite_master order by type;`

### Exporting Data

`.dump` -> outputs entire database.
The default option is to the screen (`.output stdout`). You can use `.output [filename]` to export to the file.

```sqlite
.output file.sql
.dump
.output stdout
```

> This pattern can be used to export to a file.

### Importing Data

- from SQL: `.read`
- from csv: `.import [file] [table]`

> Can use `.separator` to change the delimiter
>
> `.show` -> gives user defined settings.

Use `.read` for files created by `.dump`.

```
drop table test;
drop views schema;
.read file.sql
```

### Formatting

- `.echo` -> echoes the last run command
- `.headers` -> colum names for queries when set to 'on'
- `.null value NULL`
- `.prompt[value]`
- `mode` => csv, column, html, insert, line, list, tabs, tcl

These two code blocks do the same thing:

    .output file.csv
    .mode csv
    select * from test;
    .output stdout

and

    .output file.csv
    .separator ,
    select * from test;
    .output stdout

They output the data as a csv file.

### Exporting Delimited Data

Eg. only rows of `test` table that start with 'm' to text.csv.

    .output text.csv
    .separator ,
    select * from test where value like 'm%';
    .output stdout

Import the csv data into a similar table:

    create table test2 (id integer primary key, value text)
    .import text.csv test2

### Unattended Maintenance

These commands are used from the command line, so they can be used in automated scripts for example.

- `sqlite3 test.db .dump > test.sql`
- `sqlite3 test.db "select * from test"`
  You can read files as input stream
- `sqlite3 test2.db < test.sql`
- `sqlite3 -init test.sql test3.db .exit`
  This needs to have `.exit` so that it doesn't open the shell since it's not running a command or sql statement at the end.

### Backing up DB

SQL dump is the most portable.

`sqlite3 test.db .dump > test.sql`
