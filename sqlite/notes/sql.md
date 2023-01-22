# SQL for SQLite

The database that will be used is a collection of every food introduced in Seinfeld, and the episodes they appeared in.

![Food db tables](tables.png)

Here's the schema for the database:

    create table episodes (
    	id integer primary key,
    	season int,
    	name text
    );

    create table foods (
    	id integer primary key,
    	type_id integer,
    	name text
    );

    create table foods_episodes (
    	food_id integer,
    	episode_id integer
    );

    create table food_types (
    	id integer primary key,
    	name text
    );

Create the db with: `sqlite3 foods.db < foods.sql`

When writing SQL queries for this database, it's easier to pipe the commands from a file into the db using something like:

`sqlite3 foods.db < test.sql`

For better readability, add the following to the top of the .sql files:

    .echo on
    .mode column
    .headers on
    .null value NULL
