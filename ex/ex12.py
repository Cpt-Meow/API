import pytest
import requests


def test_headers():
    url = "https://playground.learnqa.ru/api/homework_header"
    resp = requests.get(url).headers
    print(resp)
    headers = resp
    assert headers.get('x-secret-homework-header') == "Some secret value"
