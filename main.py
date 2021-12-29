import requests

# 1
response = requests.get('https://playground.learnqa.ru/api/get_text').text
print(response)

# 2
message = requests.get('https://playground.learnqa.ru/api/get_text')
print(message.text)
