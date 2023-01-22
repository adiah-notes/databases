# The Engine

The `Engine` is an object that acts as a central source of connections to a database. Typically a global object.

Created using `create_engine()`, specify `create_engine.future` flag to `True`.

```py
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
```
> This is creating an in-memory-only SQLite database.

The string url (`sqlite+pysqlite:///:memory:`) indicates 3 things:

1. What kind of database : `sqlite` portion.
2. What DBAPI. `pysqlite` in this case.
3. How to locate the database. `/:memory:` indicates to the `sqlite3` module that it is **in-memory-only**.


# Transactions and the DBAPI

## getting a connection

`Connection` is how all interaction is done with database when working with the Core. With the ORM, it is the `Session`.
Always limit the scope of use to a specific context, with the context manager (`with`).

> Textual SQL is emitted using a construct called `text()`.

```py
>>> from sqlalchemy import text
>>> with engine.connect() as conn:
...		result = conn.execute(text("select 'hello world'"))
...		print(result.all())
```

The connection is non-autocommitting. The transaction is committed using `Connection.commit()` method.

```py
# "Commit as you go"
>>> with engine.connect() as conn:
...		conn.execute(text("CREATE TABLE some_table (x int, y int)"))
...		conn.execute(
			text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
			[{"x": 1, "y": 1}, {"x": 2, "y": 4}]
		)
		conn.commit()
```

```py
# "begin once"
>>> with engine.begin() as conn:
...		conn.execute(
...			text('INSERT INTO some_table(x,y) VALUES (:x, :y)"),
...			[{"x": 6, "y": 8}, {"x": 9, "y": 10}]
...		)
```

Using **begin once** manages the scope of the `Connection` and encloses everything inside a transaction with COMMIT at the end.

## Statement Execution

### Fetching Rows

```py
>>> with engine.connect() as conn:
...	 	result = conn.execute(text("SELECT x,y FROM some_table"))
...		for	row in result:
...			print(f"x: {row.x} y: {row.y}")
```

The object returned is called `Result` and represents an iterable object of result rows.

the `Row` objects act like named tuples.

Access the rows:

* **Tuple Assignment** -> assign variables to each row positionally as they are received

```py
result = conn.execute(text('select x, y from some_table'))

for x, y in result:
	# ...
```

* **Integer Index** -> 

```py 
result = conn.execute(text('select x,y from some_table'))

for row in result:
	x = row[0]
```

* **Attribute Name** -> 

```py 
result = conn.execute(text('select x,y from some_table'))

for row in result:
	y = row.y

	# illustrate use with Python f-strings
	print(f"Row: {row.x} {y}")
```

* Mapping Access -> 

### Sending Parameters

The `Connection.execute()` method accepts parameters.
Using a WHERE criteria that names a new parameter. the `text()` construct accepts using a colon format.
The actual value is then passed as the second argument to `Connection.execute()` in the form of a dictionary.

```py
>>> with engine.connect() as conn:
...		result = conn.execute(
...			text("SELECT x, y FROM some_table WHERE y > :y"),
...			{"y": 2}
...		)
...		for row in result:
...			print(f"x: {row.x} y: {row.y}")
```

### Sending Multiple Parameters

For statements that operate upon data but do not return result sets, we can send **multi params** to `Connection.execute()`.
Pass a list of dictionaries instead of a single dictionary.

```py
>>> with engine.connect() as conn:
...		conn.execute(
...			text("INSERT INTO some_table (x,y) VALUES (:x, :y)"),
...			[{"x": 11, "y": 12}, {"x": 13, "y": 14}]
...		)
...		conn.commit()
```

### Bundling Parameters with a Statement

```py
>>> stmt = text('SELECT x, y FROM some_table WHERE y > :y ORDER BY x,y').bindparams(y=6)
>>> with engine.connect() as conn:
...		result = conn.execute(stmt)
...		for row in result:
...			print(f"x: {row.x} y: {row.y}")
```

## Executing with an ORM Session

`Session` is the interactive object when using the ORM. Used similar to `Connection`.

```py
>>> from sqlalchemy.orm import Session

>>> stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
>>> with Session(engine) as session:
...		result = session.execute(stmt)
...		for row in result:
...			print(f"x: {row.x} y: {row.y}")
```

Can use "commit as you go"

```py
>>> with Session(engine) as session:
...		result = session.execute(
...			text("UPDATE some_table SET y=:y WHERE x=:x"),
...			[{"x": 9, "y":11}, {"x": 13, "y": 15}]
...		)
...		session.commit()
```


# Working with Database Metadata

## Setting up MetaData with Table objects

SQL Expression Language. Foundation for queries are Python object that represent database concepts like tables and columns.
`MetaData`, `Table`, and `Column`.

Collection that we place tables in called the `MetaData` object.
A facade around a Python dictionary that stores a series of `Table` objects.

```py
>>> from sqlalchemy import MetaData
>>> metadata_obj = MetaData()
```

It's most common to have a single `MetaData` Object for an entire application.

Can declare some `Table` objects.
A `user` table and an `address` table representing a list of email addresses associated with rows in the `user` table.

```py
>>> from sqlalchemy import Table, Column, Integer, String
>>> user_table = Table(
...		"user_account",
...		metadata_obj,
...		Column('id', Integer, primary_key=True),
...		Column('name', String(30)),
...		Column('fullname', String)
...	)
```

Looks like a SQL CREATE TABLE statement.
* `Table` - a database table and assigns itself to a `MetaData` collection

* `Column` - a column in a database table and assigns itself to a `Table` object.
Usually includes a string name and a type object.
The collection of `Column` objects in terms of the parent `Table` are typically accessed via an associative array located at `Table.c`

```py
>>> user_table.c.name
Column('name', String...)

>>> user_table.c.keys()
['id', 'name', 'fullname']
```

`Integer`, `String` -> SQL datatypes and can be passed to a `Column`.


## Declaring Simple Constraints

The `Column.primary_key` parameter is a shorthand technique of indicating that this `Column` is part of the primary key.
The primary key itself is normally declared implicitly and is represented by the `PrimaryKeyConstraint` construct.

```py
>>> user_table.primary_key
PrimaryKeyConstraint(Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False))
```

The most typically declared is the `ForeignKeyConstraint` object.

A `ForeignKeyConstraint` that only involves a single column on the target table is typically declared using a column-level shorthand notation.

```py
>>> from sqlalchemy import ForeignKey
>>> address_table = Table(
...		"address",
...		metadata_obj,
...		Column('id', Integer, primary_key=True),
...		Column('user_id', ForeignKey('user_account.id')),
...		Column('email_address', String, nullable=False)
...	)
```

> Another constraint `Column.nullable` to set NOT NULL

> Can omit the datatype for a `Column` with `ForeignKey` object. It is inferred.

## Emitting DDL to the Database

Emit CREATE TABLE statements (DDL) to the SQLite database.

Use the `MetaData.create_all()` method and send it the `Engine` that refers to the target db.

```py
>>> metadata_obj.create_all(engine)
```

The create process takes care of emitting CREATE statements in the correct order.

## Defining Table Metadata with ORM

### Setting up the Registry

The `MetaData` collection remains present, but it is contained within an ORM-only object known as the `registry`.

```py 
>>> from sqlalchemy.orm import registry
>>> mapper_registry = registry()
```

> Automatically includes a `MetaData` object

```py
>>> mapper_registry.metadata
MetaData()
```

Declare `Tables` indirectly through directives applied to mapped classes.
Get new declarative base from `registry` using `registry.generate_base()` method.

```py
>>> Base = mapper_registry.generate_base()
```

> Can combine into one step with `declarative_base()` function
> 
> ```py
> from sqlalchemy.orm import declarative_base
> Base = declarative_base()
>```


### Declaring Mapped Classes

The `Base` object is a Python class that serves as the base class for the ORM mapped classes we declare.

```py
>>> from sqlalchemy.orm import relationship
>>> class User(Base):
...		__tablename__ = 'user_account'
...		
...		id = Column(Integer, primary_key=True)
...		name = Column(String(30))
...		fullname = Column(String)
...
...		addresses = relationship("Address", back_populates="user")
...
...		def __repr__(self):
...			return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

>>> class Address(Base):
...		__tablename__ = 'address'
...
...		id = Column(Integer, primary_key=True)
...		email_address = Column(String, nullable=False)
...		user_id = Column(Integer, ForeignKey('user_account.id'))
...
...		user = relationship("User", back_populates="addresses")
...
...		def __repr__(self):
...			return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

The above classes are mapped and are available for use in ORM.
They also include `Table` objects that were generated.

```py
>>> User.__table__
Table('user_account', MetaData(),
	Column('id', Integer(), table=<user_account>, primary key=)
	...
)
```


### Other Mapped Class Details

* The classes have an automatically generated `__init__()` method.

```py
>>> sandy = User(name="sandy", fullname="Sandy Cheeks")
```

* `__repr__()` method is fully optional.

```py
>>> sandy
User(id=None, name='sandy', fullname='Sandy Cheeks')
```

the `id` attribute automatically returns `None` when accessed.


* a bidirectional relationship using `relationship()` on both classes.

### Emitting DDL to the database

Not any different to emitting with Core.
Can still use `MetaData.create_all()`.

```py
# emit CREATE statements given ORM registry
mapper_registry.metadata.create_all(engine)

# the identical MetaData object is also present on the 
# declarative base
Base.metadata.create_all(engine)
```

### Combining Core Table Declarations with ORM Declarative

an also make use of the `Table` objects created in conjunction with declarative mapped classes from a `declarative_base()` generated base class.

This is called `hybrid table` and consists of assigning to the `.__table__` attribute directly.

```py
mapper_registry = registry()
Base = mapper_registry.generate_base()

class User(Base):
	__table__ = user_table

	addresses = relationship("Address", back_populates="user")

	def __repr__(self):
		return f"User({self.name!r}, {self.fullname!r})"

class Address(Base):
	__table__ = address_table

	user = relationship("User", back_populates="addresses")

	def __repr__(self):
		return f"Address({self.email_address!r})"
```

### Table Reflection

Table reflection is the process of generating `Table` and related objects by reading the current state of a database.

```py
>>> some_table = Table("some_table", metadata_obj, autoload_with=engine)
```

# Working with Data

## Inserting Rows with Core

An SQL `INSERT` statement is generated using the `insert()` function.
Generates a new instance of `Insert` which represents an `INSERT` statement in SQL.


### the `insert()` SQL Expression Construct

```py
>>> from sqlalchemy import insert
>>> stmt = insert(user_table).values(name='spongebob', fullname="Spongebob Squarepants")
```

Most SQL expressions can be stringified in place as a means to see the general form of what's being produced.

```py
>>> print(stmt)
INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
```

### Executing the Statement

```py
>>> with engine.connect() as conn:
...		result = conn.execute(stmt)
...		conn.commit()
```

The `INSERT` statement above does not return any rows.


### `INSERT` usually generates the "values" clause automatically


The usual way that `Insert` is used generates this automatically.

```py
>>> with engine.connect() as conn:
...		result = conn.execute(
...			insert(user_table),
...			[
...				{"name": "sandy", "fullname": "Sandy Cheeks"},
...				{"name": "patrick", "fullname": "Patrick Star"}
...			]
...		)
...		conn.commit()
```

Don't need to do this

```py
from sqlalchemy import select, bindparam
scalar_subq = (
	select(user_table.c.id).
	where(user_table.c.name==bindparam('username')).
	scalar_subquery()
)

with engine.connect() as conn:
	result = conn.execute(
		insert(address_table).values(user_id=scalar_subq),
		[
			{}
			{"username": 'spongebob', "email_address": "spongebob@sqlalchemy.org"},
			{"username": 'sandy', "email_address": "sandy@sqlalchemy.org"},
			{"username": 'sandy', "email_address": "sandy@squirrelpower.org"},
		]
	)
	conn.commit()
```

### INSERT ... FROM SELECT

Can compose an INSERT that gets rows directly from a SELECT using the `Insert.from_select()` method:

```py
select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
	["user_id", "email_address"], select_stmt
)
print(insert_stmt)
```

### INSERT...RETURNING

```py
insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
print(insert_stmt)
```

## Selecting Rows with Core or ORM

The `select()` function generates a `Select` construct.


### The `select()` SQL Expression Construct

```py
from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == 'spongebob')
print(stmt)
```

To actually run the statement, pass it to an execution method. Iterate the result object to get `Row` objects.

```py
with engine.connect() as conn:
	for row in conn.execute(stmt):
		print(row)
```


When using the ORM, execute it using the `Session.execute()` method.

```py
stmt = select(User).where(User.name == 'spongebob')
with Session(engine) as session:
	for row in session.execute(stmt):
		print(row)
```

### Setting the COLUMNS and FROM clause

