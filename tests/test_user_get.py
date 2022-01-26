from lib_project.my_requests import MyRequests
import pytest
from lib_project.base_case import BaseCase
from lib_project.assertions import Assertions


@allure.epic("GET cases")
class TestUserGet(BaseCase):

    @allure.description("trying to get user data when the user is not logged in.")
    def test_user_details_not_auth(self):

        resp = MyRequests.get('/user/2')

        Assertions.assert_json_has_key(resp, 'username')
        Assertions.assert_json_has_no_key(resp, 'email')
        Assertions.assert_json_has_no_key(resp, 'firstName')
        Assertions.assert_json_has_no_key(resp, 'lastName')

    @allure.description("get the data of the authorized user")
    def test_user_details_auth_as_same_user(self):

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        resp1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(resp1, 'auth_sid')
        token = self.get_header(resp1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(resp1, 'user_id')

        resp2 = MyRequests.get(f'/user/{user_id_from_auth_method}',
                             headers={'x-csrf-token': token},
                             cookies={'auth_sid': auth_sid})

        expected_fields = ['username', 'email', 'firstName', 'lastName']

        Assertions.assert_json_has_keys(resp2, expected_fields)

    @allure.description("trying to get user data when logging in as another user")
    def test_other_users_data(self):
        # 1
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        res1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(res1, 'auth_sid')
        token = self.get_header(res1, 'x-csrf-token')

        data2 = self.prepare_registration_data()

        res2 = MyRequests.post("/user/", data=data2)

        Assertions.assert_code_status(res2, 200)
        Assertions.assert_json_has_key(res2, "id")
        user_id2 = self.get_json_value(res2, "id")

        res3 = MyRequests.get(f"/user/{user_id2}",
                               headers={'x-csrf-token': token},
                               cookies={'auth_sid': auth_sid})
        Assertions.assert_json_has_key(res3, "username")
        Assertions.assert_json_has_no_key(res3, "firstName")
        Assertions.assert_json_has_no_key(res3, "lastName")
        Assertions.assert_json_has_no_key(res3, "email")
