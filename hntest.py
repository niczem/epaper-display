import requests
response = requests.get("https://node-hnapi.herokuapp.com/news")
response_json = response.json()

for article in response_json:
	print(article['time_ago'])
