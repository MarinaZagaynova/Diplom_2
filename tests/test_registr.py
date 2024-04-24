import pytest
import requests as requests
import allure

from tests.data import email, password, name, empty
from tests.endpoints import Endpoints


@allure.suite('Проверка регистрации пользователем')
class TestRegistr:
    @allure.title('Создание уникального пользователя')
    @allure.description('Создание пользователя реализовано с использованием рандомных валидных значений')
    def test_creating_unique_user_success(self):
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(Endpoints.url + Endpoints.registration, json=payload)
        assert response.status_code == 200 and '"success":true' in response.text

    @allure.title('Проверка ошибки создания пользователя, который уже зарегистрирован.')
    def test_creating_double_user_error(self):
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        requests.post(Endpoints.url + Endpoints.registration, json=payload)
        response = requests.post(Endpoints.url + Endpoints.registration, json=payload)
        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.title(
        'Проверка ошибки создания пользователя без без одного из обязательных параметров. запрос возвращает ошибку')
    @pytest.mark.parametrize('emails, passwords, names', [
        (email, empty, name),
        (empty, password, name),
        (email, password, empty)])
    def test_creating_user_empty_data_error(self, emails, passwords, names):
        payload = {
            "email": emails,
            "password": passwords,
            "name": names
        }
        response = requests.post(Endpoints.url + Endpoints.registration, json=payload)
        assert response.status_code == 403 and response.text == '{"success":false,"message":"Email, password and name are required fields"}'
