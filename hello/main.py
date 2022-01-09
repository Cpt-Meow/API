import requests
from json.decoder import JSONDecodeError

# 1
response = requests.get("https://playground.learnqa.ru/api/get_text").text
print(response)

# 2
message = requests.get("https://playground.learnqa.ru/api/get_text")
print(message.text)

# 2.6
response = requests.get('https://playground.learnqa.ru/api/get_text')
print(response.text)

try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Response is not JSON format")
