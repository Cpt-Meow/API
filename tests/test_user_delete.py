from lib_project.my_requests import MyRequests
import pytest
from lib_project.base_case import BaseCase
from lib_project.assertions import Assertions


class TestUserDelete(BaseCase):

    def test_id2_delete(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        resp = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(resp, "auth_sid")
        token = self.get_header(resp, "x-csrf-token")
        user_id = self.get_json_value(resp, "user_id")

        resp2 = MyRequests.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data=data
                                  )

        Assertions.assert_code_status(resp2, 400)
        assert resp2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
                                                    f"Unexpected response content '{resp2.content}'"

    def test_user_delete(self):

        # create
        user_data = self.prepare_registration_data()

        resp = MyRequests.post("/user/", data=user_data)

        Assertions.assert_code_status(resp, 200)
        Assertions.assert_json_has_key(resp, "id")

        email = user_data["email"]
        password = user_data["password"]
        user_id = self.get_json_value(resp, "id")

        # logged in
        login_data = {
            'email': email,
            'password': password
        }

        resp2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        # del
        resp3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      data=login_data
                                  )

        Assertions.assert_code_status(resp3, 200)

        # confirm that the user is not
        resp4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(resp4, 404)
        assert resp4.content.decode("utf-8") == f"User not found", f"Unexpected response content '{resp4.content}'"

    def test_delete_by_another_user(self):
        # user 1 (auth)
        user1_data = self.prepare_registration_data()
        resp1 = MyRequests.post("/user/", data=user1_data)
        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")

        user1_id = self.get_json_value(resp1, "id")
        user1_email = user1_data["email"]
        user1_pass = user1_data["password"]

        # user 2
        user2_data = self.prepare_registration_data()
        resp2 = MyRequests.post("/user/", data=user2_data)
        Assertions.assert_code_status(resp2, 200)
        Assertions.assert_json_has_key(resp2, "id")

        user2_id = self.get_json_value(resp2, "id")
        user2_email = user2_data["email"]
        user2_pass = user2_data["password"]

        # user 1 is logged in
        login_data1 = {
            'email': user1_email,
            'password': user1_pass
        }

        resp3 = MyRequests.post("/user/login", data=login_data1)
        auth_sid_1 = self.get_cookie(resp3, 'auth_sid')
        token_1 = self.get_header(resp3, 'x-csrf-token')

        result_delete = MyRequests.delete(f"/user/{user2_id}",
                                     headers={"x-csrf-token": token_1},
                                     cookies={"auth_sid": auth_sid_1})

        Assertions.assert_code_status(result_delete, 200)

        # user 2 is logged in
        login_data2 = {
            'email': user2_email,
            'password': user2_pass
        }

        resp4 = MyRequests.post("/user/login", data=login_data2)
        auth_sid_2 = self.get_cookie(resp4, 'auth_sid')
        token_2 = self.get_header(resp4, 'x-csrf-token')

        result_delete2 = MyRequests.delete(f"/user/{user1_id}",
                                          headers={"x-csrf-token": token_2},
                                          cookies={"auth_sid": auth_sid_2})

        Assertions.assert_code_status(result_delete2, 200)

        resp5 = MyRequests.get(f"/user/{user1_id}",
                                   headers={'x-csrf-token': token_1},
                                   cookies={'auth_sid': auth_sid_1})

        print(resp5.text)

        resp6 = MyRequests.get(f"/user/{user2_id}",
                             headers={"x-csrf-token": token_2},
                             cookies={"auth_sid": auth_sid_2})

        assert resp6.content.decode("utf-8") == f"User not found", \
                                                    f"Unexpected response content '{resp6.content}'"
