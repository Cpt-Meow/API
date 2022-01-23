import pytest
import requests
from lib_project.base_case import BaseCase
from lib_project.assertions import Assertions


class TestUserAuth(BaseCase):

    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        self.url = "https://playground.learnqa.ru/api/user/login"
        self.url2 = "https://playground.learnqa.ru/api/user/auth"

        response1 = requests.post(self.url, data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_user_auth(self):
        response2 = requests.get(
            self.url2,
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookies":
            response2 = requests.get(self.url2, headers={'x-csrf-token': self.token})
        else:
            response2 = requests.get(self.url2, cookies={'auth_sid': self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
