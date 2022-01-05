import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
print(response.url)
print(response.status_code)
print(response.history)
