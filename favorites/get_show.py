import csv
import sqlite3
from sqlite3 import Error

def main():
	# db = SQL('sqlite:///favorites.db')
	database = 'favorites.db'
	title = input('Title: ').strip()

	conn = create_connection(database)
	with conn:
		select_show_by_title(conn, title)

	# rows = db.execute('SELECT COUNT(*) AS counter FROM favorites WHERE title LIKE ?', title)

	# row = rows[0]

	# print(row['counter'])

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


def select_show_by_title(conn, title):
	"""
	Query shows by title
	:param conn: Connection object
	:param title:
	:return:
	"""
	cur = conn.cursor()
	cur.execute('SELECT COUNT(*) AS counter FROM favorites WHERE title LIKE ?', (title,))

	rows = cur.fetchall()
	row = rows[0]
	# print(row['counter'])
	print(row[0])

	# for row in rows:
	# 	print(row)

if __name__ == '__main__':
	main()