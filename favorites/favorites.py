import csv

# titles = set()
titles = {}

with open('favorites.csv', 'r') as file:
	reader = csv.DictReader(file)

	for row in reader:
		title = row['title'].strip().title()
		# titles.add(title)

		if title in titles:
			titles[title] += 1
		else:
			titles[title] = 1
		
# def get_value(title):
# 	return titles[title]

for title in sorted(titles, key=lambda title: titles[title], reverse=True):
	print(title, titles[title])