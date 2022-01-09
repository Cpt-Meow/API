import requests

# Делает запрос любого типа без параметра method. Вывод: 'Wrong method provided'
response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type')
print(response.text)


# Делает запрос не из списка. Например, HEAD. Вывод: пустая строка
response = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type')
print(response.text)


# Делает запрос с правильным значением method. Вывод: {"success":"!"}
params1 = {'method': 'GET'}
response1 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=params1)
print(response1.text)

params2 = {'method': 'POST'}
response2 = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data=params2)
print(response2.text)


# С помощью цикла проверяет все возможные сочетания реальных типов запроса.
line = {'GET', 'POST', 'PUT', 'DELETE'}
for i in line:
    if i == 'GET':
        response1 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method': 'GET'})
        print(response1.text)
        response2 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method': 'POST'})
        print(response2.text)
        response3 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method': 'PUT'})
        print(response3.text)
        response4 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type',
                                 params={'method': 'DELETE'})
        print(response4.text)
    elif i == 'POST':
        response1 = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'GET'})
        print(response1.text)
        response2 = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'POST'})
        print(response2.text)
        response3 = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'PUT'})
        print(response3.text)
        response4 = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type',
                                 data={'method': 'DELETE'})
        print(response4.text)
    elif i == 'PUT':
        response1 = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'GET'})
        print(response1.text)
        response2 = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type',
                                  data={'method': 'POST'})
        print(response2.text)
        response3 = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'PUT'})
        print(response3.text)
        response4 = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type',
                                  data={'method': 'DELETE'})
        print(response4.text)
    elif i == 'DELETE':
        response1 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'GET'})
        print(response1.text)
        response2 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type',
                                  data={'method': 'POST'})
        print(response2.text)
        response3 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'PUT'})
        print(response3.text)
        response4 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type',
                                  data={'method': 'DELETE'})
        print(response4.text)
