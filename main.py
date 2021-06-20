import json
import requests
import csv


def raw_data_to_csv_format(subject,temporal_data):
	temporal_processed_data = []
	for book in temporal_data:
		temporal_processed_data.append({
			'subject': subject,
			'title': book["name"],
			'author': book['persons'][0]['name'] if book['persons'][0] else "",
			'appearances': book["appearances"],
			'score': book["score"]
		})
	return temporal_processed_data


USER_AGENT_DATA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

subjects = [
	'English Literature',
	'Business',
	'Mathematics',
	'Psychology',
	'Computer Science',
	'Biology',
	'Economics',
	'Engineering',
	'Chemistry'
]

data_size = 100
processed_data = []
for subject in subjects:
	books_url_request = f'https://explorer-api.opensyllabus.org/v1/works.json?size={data_size}&fields={requests.utils.requote_uri(subject)}&countries=US'
	request_response = requests.get(books_url_request, headers=USER_AGENT_DATA)

	data = json.loads(request_response.text)

	processed_data.extend(raw_data_to_csv_format(subject, data['results']['works']))

header = ['subject', 'title', 'author', 'appearances', 'score']
with open("book_list.csv", "w") as book_list:
	writer = csv.DictWriter(book_list, fieldnames=header)
	writer.writeheader()
	writer.writerows(processed_data)