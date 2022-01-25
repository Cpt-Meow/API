from lib_project.my_requests import MyRequests
import pytest
from lib_project.base_case import BaseCase
from lib_project.assertions import Assertions


class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        resp1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, 'id')

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(resp1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        resp2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        resp3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(resp3, 200)

        # GET
        resp4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            resp4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_unauthorized_user_changes_data(self):
        # register
        register_data = self.prepare_registration_data()
        resp1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, 'id')

        user_id = self.get_json_value(resp1, "id")
        # edit
        other_name = "New name"

        result = MyRequests.put(f"/user/{user_id}",
                                data={"firstName": other_name})
        Assertions.assert_code_status(result, 400)
        assert result.content.decode("utf-8") == f"Auth token not supplied", \
                                                f"Unexpected response content: {result.content}"

    def test_another_authorized_user_changing_data(self):
        # user 1
        user1_data = self.prepare_registration_data()
        resp1 = MyRequests.post('/user/', data=user1_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, 'id')

        user1_id = self.get_json_value(resp1, "id")
        user1_email = user1_data['email']
        user1_pass = user1_data['password']

        # user 2
        user2_data = self.prepare_registration_data()
        resp2 = MyRequests.post('/user/', data=user2_data)

        Assertions.assert_code_status(resp2, 200)
        Assertions.assert_json_has_key(resp2, 'id')

        user2_id = self.get_json_value(resp2, "id")
        user2_firstname = user2_data['firstName']

        # user 1 logged in
        login_user1 = {
            'email': user1_email,
            'password': user1_pass
        }

        result1 = MyRequests.post('/user/login', data=login_user1)

        auth_sid = self.get_cookie(result1, "auth_sid")
        token = self.get_header(result1, "x-csrf-token")

        # edit
        other_name = "New name"

        result_edit = MyRequests.put(
                f"/user/{user2_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": other_name}
        )
        print(result_edit.content)

        Assertions.assert_code_status(result_edit, 200)
        assert result_edit.content.decode("utf-8") == f"", f"Unexpected response content '{result_edit.content}'"

    def test_change_email_to_invalid(self):
        user1_data = self.prepare_registration_data()
        resp1 = MyRequests.post('/user/', data=user1_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, 'id')

        user1_id = self.get_json_value(resp1, "id")
        user1_email = user1_data['email']
        user1_pass = user1_data['password']
        user1_firstname = user1_data['firstName']

        login_user1 = {
            'email': user1_email,
            'password': user1_pass
        }

        res1 = MyRequests.post('/user/login', data=login_user1)

        auth_sid = self.get_cookie(res1, "auth_sid")
        token = self.get_header(res1, "x-csrf-token")

        incorrect_email = user1_email.replace("@", "")
        incorrect_firstname = self.get_random_username(1)

        result_edit = MyRequests.put(f'/user/{user1_id}',
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"email": incorrect_email}
                                     )

        Assertions.assert_code_status(result_edit, 400)
        assert result_edit.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content: {result_edit.content}"

        result_edit = MyRequests.put(f'/user/{user1_id}',
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"firstName": incorrect_firstname}
                                     )

        Assertions.assert_code_status(result_edit, 400)
        Assertions.assert_json_value_by_name(result_edit, "error", "Too short value for field firstName",
                                             "Unexpected response for too short name")
