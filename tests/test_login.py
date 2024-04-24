import allure
import requests

from tests.data import email, password
from tests.endpoints import Endpoints
from tests.helps import success_registration


@allure.suite('Проверка авторизации пользователем')
class TestLogin:

    @allure.title('Проверка получения ошибки под неверным логином и паролем')
    def test_login_error(self):
        payload = {
            "email": email,
            "password": password}
        response = requests.post(Endpoints.url + Endpoints.login, json=payload)
        assert response.status_code == 401 and response.text == '{"success":false,"message":"email or password are incorrect"}'

    @allure.title('Проверка успешной авторизации под существующим пользователем')
    def test_login_success(self):
        response = success_registration()
        assert response.status_code == 200 and '"success":true' in response.text
