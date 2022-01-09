import time
import requests

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

response = requests.get(url)
print(response.json())

response_json = response.json()
token = response_json['token']
seconds = response_json['seconds']
print(token, seconds)


response1 = requests.get(url, params={'token': token})
response1_json = response1.json()
status = response1_json['status']
print(status)

if status == 'Job is NOT ready':
    time.sleep(seconds)
    print(seconds)
    response2 = requests.get(url, params={'token': token})
    response2_json = response2.json()
    status = response2_json['status']

    if status == 'Job is ready':
        print('Задача готова')
    else:
        print('Задача не готова')
else:
    print('Задача готова')
