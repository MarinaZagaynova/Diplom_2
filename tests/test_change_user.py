import allure
import requests

from tests.data import email, password, name
from tests.endpoints import Endpoints
from tests.helps import get_token


@allure.suite('Проверка изменения данных пользователя')
class TestChangeUser:

    @allure.title('Проверка изменения данных, если пользователь не авторизован')
    def test_changing_user_error(self):
        new_payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.patch(Endpoints.url + Endpoints.change, data=new_payload)
        assert response.status_code == 401
        assert response.text == '{"success":false,"message":"You should be authorised"}'

    @allure.title('Проверка изменения данных, если пользователь авторизован')
    def test_changing_user_success(self):
        token = get_token()
        headers = {'Authorization': token}
        payload = {"email": email,
                   "password": password,
                   "name": name
                   }
        response = requests.patch(Endpoints.url + Endpoints.change,
                                  headers=headers, json=payload)
        assert "user" in response.text
