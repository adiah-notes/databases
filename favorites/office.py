import csv

counter = 0

with open('favorites.csv', 'r') as file:
	reader = csv.DictReader(file)

	for row in reader:
		title = row['title'].strip().title()
		# if title == 'The Office':
		if 'Office' in title:
			counter += 1

print(f'Number of people who like The Office {counter}')