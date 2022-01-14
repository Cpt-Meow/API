import pytest
import requests


def test_cookies():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    resp = requests.get(url).cookies
    print(dict(resp))
    cookies = dict(resp)

    assert cookies.get("HomeWork") == 'hw_value'
