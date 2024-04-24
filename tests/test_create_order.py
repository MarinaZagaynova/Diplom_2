import random

import allure
import pytest
import requests

from tests.endpoints import Endpoints
from tests.helps import get_token, get_ingredients


@allure.suite('Создание заказа с различными параметрами')
class TestCreateOrder:
    @allure.title('Проверка создания заказа авторизованным пользователем')
    @pytest.mark.parametrize('index', [0, 1])
    def test_create_order_authorization(self, index):
        token = get_token()
        ingredients = get_ingredients()
        payload = {"ingredients": [ingredients[index]]}
        response = requests.post(Endpoints.url + Endpoints.orders, headers={'Authorization': token}, json=payload)
        assert response.status_code == 200
        assert "number" in response.text

    @allure.title('Проверка создания заказа без авторизации пользователя.')
    @pytest.mark.parametrize('index', [0, 1])
    def test_create_order_not_authorization_single_ingredient(self, index):
        ingredients = get_ingredients()
        payload = {"ingredients": [ingredients[index]]}
        response = requests.post(Endpoints.url + Endpoints.orders, json=payload)
        assert response.status_code == 200
        assert "number" in response.text

    @allure.title('Проверка создания заказа без авторизации пользователя с тремя рандомными ингредиентами.')
    def test_create_order_not_authorization_random_ingredients(self):
        ingredients = get_ingredients()
        payload = {"ingredients": random.sample(ingredients, 3)}
        response = requests.post(Endpoints.url + Endpoints.orders, json=payload)
        assert response.status_code == 200
        assert "number" in response.text

    @allure.title('Проверка ошибки создания заказа с пустым списком ингредиентов')
    def test_create_order_without_ingredients(self):
        payload = {"ingredients": []}
        response = requests.post(Endpoints.url + Endpoints.orders, json=payload)
        assert response.status_code == 400
        assert response.text == '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title('роверка ошибки создания заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_ingredients(self):
        payload = {"ingredients": ['asasf', 'afasfa']}
        response = requests.post(Endpoints.url + Endpoints.orders, json=payload)
        assert response.status_code == 500
        assert "Internal Server Error" in response.text
