# Imports titles and genres from CSV into a SQLite database

import csv
import sqlite3
from sqlite3 import Error

def main():
	database = 'favorites8.db'

	# db.execute("CREATE TABLE shows (id INTEGER, 
	# title TEXT NOT NULL, PRIMARY KEY(id))")
	# db.execute("CREATE TABLE genres (show_id INTEGER, 
	# genre TEXT NOT NULL, FOREIGN KEY(show_id) REFERENCES shows(id))")


	sql_create_shows_table = """
		  					CREATE TABLE IF NOT EXISTS
							shows(
								id integer PRIMARY KEY,
								title text NOT NULL
							);
							"""

	sql_create_genres_table = 	"""
								CREATE TABLE IF NOT EXISTS
								genres(
									show_id integer NOT NULL,
									genre text NOT NULL,
									FOREIGN KEY (show_id)
									REFERENCES shows(id)
								);
								"""

	# create the database connection
	conn = create_connection(database)

	# if conn is not None:
	# 	create_table(conn, sql_create_genres_table)

	# 	create_table(conn, sql_create_shows_table)

	# else:
	# 	print("Error! Cannot create the database connection.")

	with conn:
		if conn is not None:
			create_table(conn, sql_create_genres_table)

			create_table(conn, sql_create_shows_table)

		else:
			print("Error! Cannot create the database connection.")

	 
	# Open CSV file
	with open("favorites.csv", "r") as file:

		# Create DictReader
		reader = csv.DictReader(file)

		# Iterate over CSV file
		for row in reader:

			# Canoncalize title
			title = row["title"].strip().upper()

			with conn:
				# Insert title
				# show_id = db.execute("INSERT INTO shows (title) VALUES(?)", title)
				show = (title,)
				show_id = add_show(conn, show)

				# Insert genres
				for genre in row["genres"].split(", "):
				# 	db.execute("INSERT INTO genres (show_id, genre) VALUES(?, ?)", show_id, genre)
					data = (show_id, genre)
					add_genre(conn, data)

# Create database

# open("favorites8.db", "w").close()
# db = cs50.SQL("sqlite:///favorites8.db")

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
		

# Create tables

# db.execute("CREATE TABLE shows (id INTEGER, title TEXT NOT NULL, PRIMARY KEY(id))")
# db.execute("CREATE TABLE genres (show_id INTEGER, genre TEXT NOT NULL, FOREIGN KEY(show_id) REFERENCES shows(id))")

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


def add_show(conn, show):
	"""
	Create a new show into the shows table
	:param conn:
	:param show:
	:return: show id
	"""

	sql = ''' INSERT INTO shows (title) VALUES(?)'''
	cur = conn.cursor()
	cur.execute(sql, show)
	conn.commit()
	return cur.lastrowid

def add_genre(conn, genre):
	"""
	Create a genre
	:param conn:
	:param genre:
	:return:
	"""

	sql = ''' INSERT INTO genres (show_id, genre) VALUES(?, ?) '''
	cur = conn.cursor()
	cur.execute(sql, genre)
	conn.commit()

	return cur.lastrowid

if __name__ == '__main__':
	main()