# Relational Databases

## Python and csv files

Storing the info in a dictionary such as the count of each title is like using a two column table.

| title | count |
| --- | --: |
| The Office | 15 |


keys on the left and values on the right

Flat file databases

---

### Lambda functions

Instant return value for simple function

```py
for title in sorted(titles, key=lambda title: titles[title], reverse=True):
```

## Regexes

```py
import re

...
if re.search('^(Office|The.Office)$', title):
	counter += 1
```


## SQL

CSV is like a single sheet in a spread sheet.


CRUD:

| Operation | Command |
| --- | --- |
| Create | CREATE, INSERT |
| Read 	 | SELECT |
| Update | UPDATE |
| Delete | DELETE, DROP |


Example

```SQL
CREATE TABLE table (column type, ...);
```

create a database with `sqlite3 name.db`

In `sqlite3` can use
`.mode csv`

Import csv file as table
`.import favorites.csv favorites`


``` SQL
SELECT title FROM favorites;

SELECT title, genres FROM favorites;

SELECT DISTINCT(UPPER(title)) FROM favorites;

SELECT COUNT(title) FROM favorites;


WHERE
LIKE
ORDER BY
LIMIT 
GROUP BY

SELECT title FROM favorites LIMIT;

SELECT title FROM favorites WHERE title LIKE 'office';

SELECT title FROM favorites WHERE title LIKE '%office%';

SELECT COUNT(title) FROM favorites WHERE title LIKE '%office%';

DELETE FROM favorites WHERE title LIKE '%friends%';

SELECT title FROM favorites WHERE title = 'Thevoffice';

UPDATE favorites SET title = 'The Office' WHERE title = 'Thevoffice';

SELECT genres FROM favorites WHERE title = 'Game of Thrones';

UPDATE favorites SET genres = 'Action, Adventure, Drama, Fantasy, Thriller, War' WHERE title = 'Game of Thrones';

SELECT title FROM favorites WHERE genres = 'Comedy';
-- Doesn't work when there are multiple genres
-- Could use the like '%Comedy%';
-- Not a good design for data - csv in csv
```


Load data into two tables: titles and genres.

```py
# Imports titles and genres from CSV into a SQLite database

import cs50
import csv

# Create database
open("favorites8.db", "w").close()
db = cs50.SQL("sqlite:///favorites8.db")

# Create tables
db.execute("CREATE TABLE shows (id INTEGER, title TEXT NOT NULL, PRIMARY KEY(id))")
db.execute("CREATE TABLE genres (show_id INTEGER, genre TEXT NOT NULL, FOREIGN KEY(show_id) REFERENCES shows(id))")

# Open CSV file
with open("favorites.csv", "r") as file:

    # Create DictReader
    reader = csv.DictReader(file)

    # Iterate over CSV file
    for row in reader:

        # Canoncalize title
        title = row["title"].strip().upper()

        # Insert title
        show_id = db.execute("INSERT INTO shows (title) VALUES(?)", title)

        # Insert genres
        for genre in row["genres"].split(", "):
            db.execute("INSERT INTO genres (show_id, genre) VALUES(?, ?)", show_id, genre)
```

```SQL
SELECT show_id FROM genres WHERE genre = 'Comedy';

SELECT title FROM shows WHERE id IN (SELECT show_id FROM genres WHERE genre = 'Comedy');

SELECT DISTINCT title FROM shows WHERE id IN (SELECT show_id FROM genres WHERE genre = 'Comedy') ORDER BY title;
-- Start with some subqueries

INSERT INTO shows (title) VALUES('Seinfeld');

INSERT INTO genres (show_id, genre) VALUES(159, 'Comedy');
UPDATE shows SET title = 'SEINFELD' WHERE title = 'Seinfeld';
```

## SQL in Python

```py
import csv

from cs50 import SQL

db = SQL('sqlite:///favorites.db')
title = input('Title: ').strip()

rows = db.execute('SELECT COUNT(*) AS counter FROM favorites WHERE title LIKE ?', title)

row = rows[0]

print(row['counter'])

```

## Data types

* Blob
* Integer
* Numeric
* Real
* Text

```SQL
CREATE INDEX 'title_index' ON 'shows' ('title');
-- speeds up

CREATE INDEX name ON table(column, ...);
```

Indexes are data structures that helps databases do searches. With something like a tree.

B-trees. Wide and shallow tree.

## Data across multiple tables

`JOIN`

```SQL
SELECT id FROM people WHERE name = 'Steve Carell';

SELECT show_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = 'Steve Carell');

SELECT title FROM shows WHERE id IN (SELECT show_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = 'Steve Carell'));

CREATE INDEX person_index ON stars (person_id);
CREATE INDEX show_index ON stars (show_id);
CREATE INDEX name_index ON people (name)


SELECT title FROM people JOIN stars ON people.id = stars.person_id JOIN shows ON stars.show_id = shows.id WHERE name = 'Steve Carell' ORDER BY title;

SELECT title FROM people, stars, shows
	WHERE people.id = stars.person_id
	AND stars.show_id = shows.id
	AND name = 'Steve Carell'
	ORDER BY title;

```


# Python sqlite

## Creating a database in python

Create a `Connection` object

```py
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # create_connection(r"C:\sqlite\db\pythonsqlite.db)
    create_connection('pythonsqlite.db')
```

## Creating Tables

1. Create a `Connection` object using `connect()`
2. Create a `Cursor` object using `cursor()` method of `Connection` object.
3. pass `CREATE TABLE` statement to teh `execute()` method of the `Cursor` object.

| Tasks |
| --- |
| * id |
| name |
| priority |
| status_id |
| project_id |
| begin_date |
| end_date |

| projects |
| --- |
| * id |
| name |
| begin_date |
| end_date |


These are the SQL statement to create the tables

```SQL
-- projects table
CREATE TABLE IF NOT EXISTS projects (
    id integer PRIMARY KEY,
    name text NOT NULL,
    begin_date text,
    end_date text
);

-- tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id integer PRIMARY KEY,
    name text NOT Null,
    priority integer,
    project_id integer NOT NULL,
    status_id integer NOT NULL,
    begin_date text NOT NULL,
    end_date text NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
```

First, create function that returns the `Connection` object

```py
def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
```

Second, develop `create_table()` that accepts a `Connection` object and SQL statement.

```py
def create_table(conn, create_table_sql):
    """
    Create a table from the create_table statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
```


Third, create a `main()` function to create the `projects` and `tasks` tables.

```py
def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    sql_create_projects_table = """
                                CREATE TABLE IF NOT EXISTS projects(
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    begin_date text,
                                    end_date text
                                );
                                """

    sql_create_tasks_table = """
                            CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                priority integer,
                                status_id integer NOT NULL,
                                project_id integer NOT NULL,
                                begin_date text NOT NULL,
                                end_date text NOT NULL,
                                FOREIGN KEY (project_id) REFERENCES projects (id)
                            );
                            """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")
```

Finally, execute the `main()` function.

```py
if __name__ == '__main__':
    main()
```


## Inserting Data

1. Connect to the SQLite Database by creating a `Connection` object.
2. Create a `Cursor` object
3. Execute an `INSERT` statement. Using a `?` as placeholder for each argument.

First create the function to establish  a database connection

```py
def create_connection(db_file):
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
```

Function to insert a new project into the `projects` table.

```py
def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name, begin_date, end_date) VALUES(?, ? ?)'''

    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid
```

`lastrowid` gets back the generated id.


Another function for inserting rows into the tasks table

```py
def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :ret urn:
    """

    sql = '''INSERT INTO tasks(name, priority, status_id, project_id, begin_date, end_date) VALUES(?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid
```


Develop the `main()` function

```py 
def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create database connection
    conn = create_connection(database)

    with conn:
        # create new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        project_id = create_project(conn, project)

        # tasks
        task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)
```

Call the `main()` function

```py
if __name__ == '__main__':
    main()
```

## Updating

1. Create database connection.
2. Create `Cursor`.
3. Execute `UPDATE` statement with `execute()` method of `Cursor`.

`create_connection()`

```py
def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
```

`update-task()` updates a specific task:

```py
def update_task(conn, task):
    """
    Update priority, begin_date, and end_date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
            SET priority = ?,
                begin_date = ?,
                end_date = ?
            WHERE id = ? 
        '''

    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
```

`main()` creates a connection and then calls `update_task()` on a task with id 2

```py
def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create database connection
    conn = create_connection(database)
    with conn:
        update_task(conn, (2, '2015-01-04', '2015-01-05', 2))

if __name__ == '__main__':
    main()
```

## Deleting

`delete_task()` deletes a tasks by id

```py
def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn: Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'

    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

```

`delete_all_tasks()` deletes all rows in the `tasks` table

```py
def delete_all_tasks(conn):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
```

`main()`

```py
def main():
    database = r'C:\sqlite\db\pythonsqlite.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        delete_task(conn, 2)
        # delete_all_tasks(conn)

if __name__ == '__main__':
    main()
```

## Querying

1. Create `Connection` object.
2. Create `Cursor` object.
3. Execute a `SELECT` statement.
4. Call `fetchall()` method on `Cursor`.
5. Loop the cursor and process each row individually.


This function selects all rows from the tasks table and displays the data.

```py
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')

    rows = cur.fetchall()

    for row in rows:
        print(row)
```

Query tasks by priority:

```py
def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE priority=?', (prioritiy,))

    rows = cur.fetchall()

    for row in rows:
        print(row)
```

`main()`

```py
def main():
    database = r'C:\sqlite\db\pythonsqlite.db'

    # create database connection
    conn = create_connection(database)
    with conn:
        print("1.Query task by priority:")
        select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        select_all_tasks(conn)
```