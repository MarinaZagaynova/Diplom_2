import json
import random

import allure
import requests

from tests.data import password
from tests.endpoints import Endpoints
from tests.helps import success_registration


@allure.suite('Проверка авторизации пользователем')
class TestLogin:

    @allure.title('Проверка получения ошибки под неверным логином')
    def test_login_error_login(self):
        payload = {
            "email": f"new{random.randint(1, 100000)}@gmail.com",
            "password": password}
        response = requests.post(Endpoints.url + Endpoints.login, json=payload)
        assert response.status_code == 401 and response.text == '{"success":false,"message":"email or password are incorrect"}'

    @allure.title('Проверка получения ошибки под неверным паролем')
    def test_login_error(self):
        registration = success_registration().json()
        real_email = registration['user']['email']
        payload = {
            "email": real_email,
            "password": f"password{random.randint(1, 1000000)}"}
        response = requests.post(Endpoints.url + Endpoints.login, json=payload)
        assert response.status_code == 401 and response.text == '{"success":false,"message":"email or password are incorrect"}'

    @allure.title('Проверка успешной авторизации под существующим пользователем')
    def test_login_success(self):
        response = success_registration()
        assert response.status_code == 200 and '"success":true' in response.text
