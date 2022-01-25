from lib_project.my_requests import MyRequests
import pytest
from lib_project.base_case import BaseCase
from lib_project.assertions import Assertions


class TestUserRegister(BaseCase):
    params = [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        resp = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(resp, 200)
        Assertions.assert_json_has_key(resp, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        resp = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {resp.content}"

        # run > python -m pytest -s tests/test_user_register.py

    def test_create_user_incorrect_email(self):

        email = 'vinkotovexample.com'

        data = self.prepare_registration_data(email)

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == f"Invalid email format", \
                                                f"Unexpected response content '{response.content}'"

    @pytest.mark.parametrize('key', params)
    def test_create_user_without_one_field(self, key):

        data = self.prepare_incomplete_registration_data(key)

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == f"The following required params are missed: {key}", \
                                                f"Unexpected response content '{resp.content}'"

    def test_for_short_nickname(self):

        short_nickname = self.get_random_username(1)

        data = self.prepare_registration_data()
        data['firstName'] = short_nickname

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == f"The value of 'firstName' field is too short", \
                                                f"Unexpected response content '{response.content}'"

    def test_for_long_nickname(self):

        long_nickname = self.get_random_username(355)

        data = self.prepare_registration_data()
        data['firstName'] = long_nickname

        resp = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
                                                f"Unexpected response content for field 'firstName' when it is too long"

